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
pdbID1.chain_pdbID2.chain
. indicates that only one chain should be shown
 _ indicates that more than one protein should be shown}

\item{data}{List of lists containing elements 'uploaded', 'selectedvalue', 'chain', 'color', 'filename', 'ext', 'config'.
those elements have the following types:
  - uploaded (logical; required)
  - selectedvalue (character; required)
  - chain (character; required)
  - color (character; required)
  - filename (character; required)
  - ext (character; optional)
  - config (optional): . config has the following type: lists containing elements 'type', 'input'.
those elements have the following types:
  - type (character; required)
  - input (character; required)s. The data (in JSON format) that will be used to display the molecule
selectedValue: pdbString
color: color in hex format
filename: name of the used pdb/cif file
ext: file extensions (pdb or cif)
config.input: content of the pdb file
config.type: format of config.input}
}
