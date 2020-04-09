% Auto-generated: do not edit by hand
\name{DashNglDashNgl}

\alias{DashNglDashNgl}

\title{DashNgl component}

\description{
The NglMoleculeViewer is used to render schematic diagrams of biomolecules in ribbon-structure representations. Read more about the used WebGL protein viewer here: https://github.com/arose/ngl
}

\usage{
DashNglDashNgl(id=NULL, viewportStyle=NULL, stageParameters=NULL, pdbString=NULL, data=NULL)
}

\arguments{
\item{id}{Character. The ID of this component, used to identify dash components in callbacks.
The ID needs to be unique across all of the components in an app.}

\item{viewportStyle}{Lists containing elements 'width', 'height'.
those elements have the following types:
  - width (character; optional)
  - height (character; optional). The height and the width (in px) of the container
in which the molecules will be displayed.
Default: width:1000px / height:500px
It should be in JSON format.}

\item{stageParameters}{Lists containing elements 'quality', 'backgroundcolor', 'cameratype'.
those elements have the following types:
  - quality (character; optional)
  - backgroundcolor (character; optional)
  - cameratype (character; optional). Parameters (in JSON format) for the stage object of ngl.
Currently implemented are the quality of the visualisation
and the background colorFor a full list see:
http://nglviewer.org/ngl/api/file/src/stage/stage.js.html}

\item{pdbString}{Character. Variable which defines how many molecules should be shown and/or which chain
The following format needs to be used:
pdbID1.chain:start-end_pdbID2.chain:start-end
. indicates that only one chain should be shown
: indicates that a specific range should be shown (e.g. 1-50)
 _ indicates that more than one protein should be shown}

\item{data}{List of lists containing elements 'filename', 'ext', 'selectedvalue', 'chain', 'range', 'color', 'config', 'resetview', 'uploaded'.
those elements have the following types:
  - filename (character; required)
  - ext (character; optional)
  - selectedvalue (character; required)
  - chain (character; required)
  - range (character; required)
  - color (character; required)
  - config (optional): . config has the following type: lists containing elements 'type', 'input'.
those elements have the following types:
  - type (character; required)
  - input (character; required)
  - resetview (logical; required)
  - uploaded (logical; required)s. The data (in JSON format) that will be used to display the molecule
filename: name of the used pdb/cif file
ext: file extensions (pdb or cif)
selectedValue: pdbString
chain: selected chain
range: selected range
color: color in hex format
config.input: content of the pdb file
config.type: format of config.input
resetView: bool if the view should be resettet
uploaded: bool if the file was uploaded}
}
