import React, {Component} from 'react';
import PropTypes from 'prop-types'; //exports a range of data validators 
import { Stage } from 'ngl'; //https://github.com/arose/ngl/blob/master/src/stage/stage.ts
/**
 * Dash ngl component
 */
export default class DashNgl extends Component {

  //constructor might not be needed anylonger:
  //https://hackernoon.com/the-constructor-is-dead-long-live-the-constructor-c10871bea599
  constructor(props) {
    super(props); //initiate the parent's constructor method and allows the component to inherit methods from its parent
    this.state = {stage: null, structuresList:[]} // initial values are set
    console.log(this.props)
    console.log(this.state)
  }
  
  //called after the component is rendered
  componentDidMount() {
    const { id, stageParameters } = this.props;
    const stage = new Stage(id, stageParameters);
    const structuresList=[]
    this.setState({ stage })
  }     

  //triggered by any update of the DOM (e.g. new dropdown selection)
  shouldComponentUpdate(nextProps) {
    const { id, stageParameters } = this.props;
    let filename = this.props.data.filename;
    const { stage } = this.state;

    if (filename !== nextProps.data.filename){
      return true //go to componentDidUpdate()
    }
    else{
      return false //viewer will not be updated
    }
  }
  
  //called only if shouldComponentUpdate evaluates to true
  componentDidUpdate() {
    console.log("updated")
    const { data } = this.props;
    const { stage, structuresList} = this.state;
    let filename = data.filename

    console.log(structuresList)

    if (data.filename!='placeholder'){
      console.log(filename)
      stage.eachComponent(function(comp) {comp.removeAllRepresentations()})

      if(structuresList.includes(filename)) {
        this.loadStructure(stage,filename)
      }
      else{
        this.loadData(stage,data,structuresList)
      }
    }
  }

  //helper functions which styles the output of loadStructure/loadData 
  showStructure(stageObj) {
    stageObj.addRepresentation("cartoon")
    stageObj.autoView()
  }

  //If user has selected structure already just add the new Representation 
  loadStructure(stage,filename){
    console.log("load from browser")
    let stageObj=stage.getComponentsByName(filename)
    this.showStructure(stageObj)
  }

  //If not load the structure from the backend
  loadData(stage,data,structuresList) {
    console.log("load from backend")
    const stringBlob = new Blob([data.config.input], { type: data.config.type })
    stage.loadFile(stringBlob, { ext: data.ext, defaultRepresentation: false }).then(stageObj => {
        this.showStructure(stageObj);
        stageObj.name=data.filename;
        
        this.setState(state => ({
          structuresList: state.structuresList.concat([data.filename])
        }));
        console.log(this.state)
    });
  }
  
  render() {
    const { id,viewportStyle } = this.props;
    const style = { ...defaultViewportStyle }; //...expands defaultViewportStyle
    
    return (
      <div id='viewport' style={style} />
    );
  }
}

const defaultViewportStyle = {
  backgroundColor: 'black',
  width: '100%',
  height: '500px',
}

const dataPropShape = {
    filename: PropTypes.string.isRequired,
    ext: PropTypes.string,
    config: PropTypes.shape({
        type: PropTypes.string.isRequired,
        input: PropTypes.oneOfType([
            PropTypes.array,
            PropTypes.object,
            PropTypes.string
        ])
    })
};

DashNgl.defaultProps = {
};

DashNgl.propTypes = {  
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * Custom property
     */
    data: PropTypes.oneOfType([ //enumerating the types of values the component can accept
        PropTypes.arrayOf(PropTypes.shape(dataPropShape)), //ensure an array (items with specified type)
        PropTypes.shape(dataPropShape) //ensures an object with specified keys with values of specified types
    ]),
};
