import React, {Component} from 'react';
import PropTypes from 'prop-types'; //exports a range of data validators
import {Stage, Selection} from 'ngl'; //https://github.com/arose/ngl/blob/master/src/stage/stage.ts

/**
 * The NglMoleculeViewer is used to render schematic diagrams
 * of biomolecules in ribbon-structure representations.
 * Read more about the used WebGL protein viewer here:
 * https://github.com/arose/ngl
 */
export default class DashNgl extends Component {
  // constructor might not be needed anylonger:
  // https://hackernoon.com/the-constructor-is-dead-long-live-the-constructor-c10871bea599
  constructor (props) {
    super(props) // initiate the parent's constructor method and allows the component to inherit methods from its parent
    this.state = { stage: null, structuresList: [] } // initial values are set
    console.log(this.props)
    console.log(this.state)
  }

  // called after the component is rendered
  componentDidMount () {
    const { id, stageParameters, viewportStyle } = this.props
    const params = { ...stageParameters }
    const stage = new Stage(id, params)
    stage.setSize(viewportStyle.width, viewportStyle.height)
    this.setState({ stage })
    console.log('component did mount')
  }

  // triggered by any update of the DOM (e.g. new dropdown selection)
  shouldComponentUpdate (prevProps, nextProps) {
    const { stageParameters, data } = this.props
    console.log(data)

    // check if data has changed
    if (data !== null & prevProps.data !== null) {
      console.log({ prevProps, nextProps })

      // wait for the first pdb selection after startup
      if (nextProps.data !== undefined) {
        console.log('first pdb selection')
        return true
      }

      // check if pdb selection has changed
      const oldSelection = prevProps.data[0].selectedValue
      const newSelection = data[0].selectedValue
      console.log({ oldSelection, newSelection })
      if (oldSelection !== newSelection) {
        console.log('pdb selection has changed')
        return true
      }

      console.log(data)
      // check if structure has been uploaded
      if (data[0].uploaded === true){
        console.log('data has been uploaded')
        return true
      }
    } 

    // check for stage params changed
    const oldStage = prevProps.stageParameters
    const newStage = stageParameters
    console.log({ oldStage, newStage })

    // save it as a helper function
    const isEqual = (obj1, obj2) => {
      const obj1Keys = Object.keys(obj1)
      const obj2Keys = Object.keys(obj2)

      if (obj1Keys.length !== obj2Keys.length) {
        return false
      }

      for (const objKey of obj1Keys) {
        if (obj1[objKey] !== obj2[objKey]) {
          return false
        }
      }

      return true
    }

    if (isEqual(oldStage, newStage) === false) {
      console.log('stage params changed')
      return true
    }
    return false
  }

  // called only if shouldComponentUpdate evaluates to true
  componentDidUpdate () {
    console.log('updated')
    const { data, stageParameters } = this.props
    const { stage, structuresList } = this.state

    console.log({ data, stageParameters })

    stage.setParameters(stageParameters)

    const newSelection = data[0].selectedValue
    console.log(structuresList)

    if (newSelection !== 'placeholder') {
      // console.log(newSelection)
      stage.eachComponent(function (comp) {
        comp.removeAllRepresentations()
      })

      this.processDataFromBackend(data, stage, structuresList)
    }
  }

  // helper functions which styles the output of loadStructure/loadData
  showStructure (stageObj, chain, color, xOffset, stage) {
    if (chain !== 'ALL') {
      const selection = new Selection(':' + chain)
      const pa = stageObj.structure.getPrincipalAxes(selection)

      // delete the invisble elements ?
      console.log(selection)
      console.log(pa)
      console.log(pa.getRotationQuaternion())
      console.log(color)

      stageObj.addRepresentation('cartoon', {
        sele: ':' + chain,
        color: color
      })
      stageObj.setRotation(pa.getRotationQuaternion())

      // translate by x angstrom along chosen axis
      stageObj.setPosition([xOffset, 0, 0])
      // stage.animationControls.rotate(pa.getRotationQuaternion(),1500)
    } else {
      stageObj.addRepresentation('cartoon')
    }
    stage.animationControls.moveComponent(stageObj, stageObj.getCenter(), 1000)
    // stage.autoView()
  }

  // If user has selected structure already just add the new Representation
  loadStructure (stage, filename, chain, color, xOffset) {
    console.log('load from browser')
    // console.log(filename)
    const stageObj = stage.getComponentsByName(filename).list[0]
    this.showStructure(stageObj, chain, color, xOffset, stage)
  }

  // If not load the structure from the backend
  processDataFromBackend (data, stage, structuresList) {
    console.log('processDataFromBackend')

    const xval1 = 0
    const xval2 = 100
    const xval3 = 200
    const xval4 = 300

    const xOffsetArr = [xval1, xval2, xval3, xval4]

    // loop over list of structures:
    for (var i = 0; i < data.length; i++) {
      const filename = data[i].filename
      // check if already loaded
      if (structuresList.includes(filename)) {
        this.loadStructure(stage,
          filename,
          data[i].chain,
          data[i].color,
          xOffsetArr[i])
      } else { // load from backend
        this.loadData(data[i], stage, structuresList, xOffsetArr[i])
      }
    }
    const center = stage.getCenter()
    const newZoom = -500
    const duration = 1000
    stage.animationControls.zoomMove(center, newZoom, duration)

    // let orientationMatrix = stage.viewerControls.getOrientation();
    // console.log(orientationMatrix)
    // stage.viewerControls.orient(orientationMatrix);

    // autoView = stage.animationControls.zoomMove(center, zoom, 0)
    // stage.animationControls.zoomMove(center, zoom, 0)

    // const center = stage.getCenter()
    // console.log(center)
    // let zoom = stage.getZoom()
    // zoom = zoom - 500
    // console.log(zoom)

    // // stage.autoView()
    // // change zoom depending on sub units
    // const zoom3 = -500
    // stage.animationControls.zoomMove(center, zoom3, 1000)
    // // stage.autoView(center,zoom,1000)

    // const center2 = stage.getCenter()
    // console.log(center2)
    // const zoom2 = stage.getZoom()
    // // zoom = zoom + 5
    // console.log(zoom2)

    // stage.viewer.zoom(distance, set)
    // let orientationMatrix2 = stage.viewerControls.getOrientation()
    // console.log(orientationMatrix2)
  }

  loadData (data, stage, structuresList, xOffset) {
    console.log('load from backend')
    const stringBlob = new Blob([data.config.input], { type: data.config.type })
    stage.loadFile(stringBlob, { ext: data.ext, defaultRepresentation: false }).then(stageObj => {
      stageObj.name = data.filename
      this.showStructure(
        stageObj,
        data.chain,
        data.color,
        xOffset,
        stage
      )

      this.setState(state => ({
        structuresList: state.structuresList.concat([
          data.filename])
      }))
      console.log(this.state)
    })
  }

  render () {
    const { id } = this.props
    return (
      <div>
        <div id={id} />
      </div>
    )
  }
}

const defaultViewportStyle = {
  width: '500x',
  height: '500px'
}

const defaultStageParameters = {
  quality: 'medium',
  backgroundColor: 'white',
  cameraType: 'perspective'
}

const defaultData = [{
  uploaded: true,
  selectedValue: 'placeholder',
  chain: 'ALL',
  color: 'red',
  filename: 'placeholder',
  ext: '',
  config: {
    type: 'text/plain',
    input: ''
  }
}]

console.log(defaultData)

DashNgl.defaultProps = {
  data: defaultData,
  viewportStyle: defaultViewportStyle,
  stageParameters: defaultStageParameters
}

DashNgl.propTypes = {
  /**
   * The ID of this component, used to identify dash components in callbacks.
   * The ID needs to be unique across all of the components in an app.
   */
  id: PropTypes.string,

  /**
   * The height and the width (in px) of the container
   * in which the molecules will be displayed.
   * Default: width:1000px / height:500px
   * It should be in JSON format.
  */
  viewportStyle: PropTypes.exact({
    width: PropTypes.string,
    height: PropTypes.string
  }),

  /**
   * Parameters (in JSON format) for the stage object of ngl.
   * Currently implemented are the quality of the visualisation
   * and the background colorFor a full list see:
   * http://nglviewer.org/ngl/api/file/src/stage/stage.js.html
   */
  stageParameters: PropTypes.exact({
    quality: PropTypes.string,
    backgroundColor: PropTypes.string,
    cameraType: PropTypes.string
  }),

  /**
   * Variable which defines how many molecules should be shown and/or which chain
   * The following format needs to be used:
   * pdbID1.chain_pdbID2.chain
   * . indicates that only one chain should be shown
   *  _ indicates that more than one protein should be shown
   */
  pdbString: PropTypes.string,

  /**
   * The data (in JSON format) that will be used to display the molecule
   * selectedValue: pdbString
   * color: color in hex format
   * filename: name of the used pdb/cif file
   * ext: file extensions (pdb or cif)
   * config.input: content of the pdb file
   * config.type: format of config.input
   */
  data: PropTypes.arrayOf(
    PropTypes.exact({
      uploaded: PropTypes.bool.isRequired,
      selectedValue: PropTypes.string.isRequired,
      chain: PropTypes.string.isRequired,
      color: PropTypes.string.isRequired,
      filename: PropTypes.string.isRequired,
      ext: PropTypes.string,
      config: PropTypes.exact({
        type: PropTypes.string.isRequired,
        input: PropTypes.string.isRequired
      })
    })
  )
}
