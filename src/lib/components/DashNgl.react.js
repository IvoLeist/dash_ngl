import React, {Component} from 'react';
import PropTypes from 'prop-types'; //exports a range of data validators 
import { Stage, Selection, PdbWriter } from 'ngl'; //https://github.com/arose/ngl/blob/master/src/stage/stage.ts

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
    const params = { ...defaultStageParameters, ...stageParameters }
    console.log(params)

    const stage = new Stage(id, params);
    
    this.setState({ stage })
    console.log("component did mount")

    //const structuresList=[]
  }     

  //triggered by any update of the DOM (e.g. new dropdown selection)
  shouldComponentUpdate(nextProps) {
    const { id, stageParameters } = this.props;

    //when the app is starting data is not correctly interpreted as an array
    //but after a few seconds it is therefore this if-else statement
    if (Array.isArray(this.props.data)==false){
      return false //viewer will not be updated 
    }
    else{
      let oldSelection = this.props.data[0].selectedValue;
      let newSelection = nextProps.data[0].selectedValue 
  
      //check for stage params changed
      if (stageParameters !== nextProps.stageParameters) {
          //console.log("stage params changed")
          //this.stage.setParameters(stageParameters)
          return true
        }
      
      //check if pdb selection has changed
      if (oldSelection !== newSelection){
        return true //go to componentDidUpdate()
      }
      else{
        return false //viewer will not be updated
      }
    }
  }
  
  //called only if shouldComponentUpdate evaluates to true
  componentDidUpdate() {
    console.log("updated")
    const { data, stageParameters } = this.props;
    const { stage, structuresList } = this.state;

    stage.setParameters(stageParameters)
    
    let newSelection = data[0].selectedValue

    console.log(structuresList)

    if (newSelection !='placeholder'){
      //console.log(newSelection)
      stage.eachComponent(function(comp) {comp.removeAllRepresentations()})

      this.processDataFromBackend(data,stage,structuresList)
    }
  }

  //helper functions which styles the output of loadStructure/loadData 
  showStructure(stageObj,chain,color,xOffset,stage) {
    //console.log(chain)

    if (chain != 'ALL'){
      let selection = new Selection( ":"+chain );
      let pa=stageObj.structure.getPrincipalAxes(selection)

      console.log(stageObj.getBox())
      console.log(stageObj.getBox(":"+chain))
      //delete the invisble elements ?

      console.log(selection)
      console.log(pa)
      console.log(pa.getRotationQuaternion())
    
      //stageObj.addRepresentation("cartoon",{color:'grey'})
      console.log(color)
      stageObj.addRepresentation("cartoon",{sele:":"+chain, color:color})
      stageObj.setRotation(pa.getRotationQuaternion())

      //translate by x angstrom along chosen axis
      stageObj.setPosition([ xOffset, 0 , 0 ])
      //stage.animationControls.rotate(pa.getRotationQuaternion(),1500)

    }
    else{
      stageObj.addRepresentation("cartoon")
    }
    stage.animationControls.moveComponent(stageObj,stageObj.getCenter(),1000)
    //stage.autoView()
  }

  //If user has selected structure already just add the new Representation 
  loadStructure(stage,filename,chain,color,xOffset){
    console.log("load from browser")
    //console.log(filename)
    let stageObj=stage.getComponentsByName(filename).list[0]
    this.showStructure(stageObj,chain,color,xOffset,stage)
  }

  //If not load the structure from the backend
  processDataFromBackend(data,stage,structuresList){
    //console.log('processDataFromBackend')
    
    const xOffsetArr = [0,100,200,300]
    //loop over list of structures:
    for (var i = 0; i < data.length; i++) {
      let filename = data[i].filename
      //check if already loaded
      if(structuresList.includes(filename)){
        this.loadStructure(stage,filename,data[i].chain,data[i].color,xOffsetArr[i])
      }
      else{ //load from backend
        this.loadData(data[i],stage,structuresList,xOffsetArr[i])
      }
    }
    //let orientationMatrix = stage.viewerControls.getOrientation();
    //console.log(orientationMatrix)
    //stage.viewerControls.orient(orientationMatrix);

    //autoView = stage.animationControls.zoomMove(center, zoom, 0)
    //stage.animationControls.zoomMove(center, zoom, 0)

    let center=stage.getCenter()
    console.log(center)
    let zoom=stage.getZoom()
    zoom = zoom - 500
    console.log(zoom)

    //stage.autoView()
    //change zoom depending on sub units
    let zoom3 = -500
    stage.animationControls.zoomMove(center,zoom3,1000) 
    //stage.autoView(center,zoom,1000)
    
    let center2=stage.getCenter()
    console.log(center2)
    let zoom2=stage.getZoom()
    //zoom = zoom + 5
    console.log(zoom2) 



    //stage.viewer.zoom(distance, set)
    // let orientationMatrix2 = stage.viewerControls.getOrientation()
    // console.log(orientationMatrix2)
  }

  loadData(data,stage,structuresList,xOffset) {
    console.log("load from backend")
    const stringBlob = new Blob([data.config.input], { type: data.config.type })
    stage.loadFile(stringBlob, { ext: data.ext, defaultRepresentation: false }).then(stageObj => {
        stageObj.name=data.filename;
        this.showStructure(stageObj,data.chain,data.color,xOffset,stage);
        
        this.setState(state => ({
          structuresList: state.structuresList.concat([data.filename])
        }));
        console.log(this.state)
    });
  }
  
  render() {
    const { id,viewportStyle } = this.props;
    const style = { ...defaultViewportStyle }; //...expands defaultViewportStyle
    //console.log(style)

    return (
      <div>
        <div id='viewport' style={style}/>
      </div>
    );
  }
}

const defaultViewportStyle = {
  width: '100%',
  height: '500px',
}

const defaultStageParameters = {
    quality: 'medium',
    backgroundColor: 'white'
}

const dataPropShape = {
    selectedValue:PropTypes.string.isRequired,
    chain:PropTypes.string.isRequired,
    color:PropTypes.string.isRequired,
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
    id: 'viewport',
    viewportStyle: defaultViewportStyle,
    stageParameters: defaultStageParameters,
};

DashNgl.propTypes = {  
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * CSS styling for viewport container
     */
    viewportStyle: PropTypes.object,

    /**
     * Parameters for the stage
     */
    stageParameters: PropTypes.object,

    /**
     * Custom property
     */
    data: PropTypes.oneOfType([ //enumerating the types of values the component can accept
            PropTypes.arrayOf(PropTypes.shape(dataPropShape)), //ensure an array (items with specified type)
            PropTypes.shape(dataPropShape) //ensures an object with specified keys with values of specified types
            ]),
};
