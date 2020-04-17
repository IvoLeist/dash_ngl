# AUTO GENERATED FILE - DO NOT EDIT

DashNglDashNgl <- function(id=NULL, viewportStyle=NULL, stageParameters=NULL, imageParameters=NULL, downloadImage=NULL, pdbString=NULL, data=NULL, molStyle=NULL) {
    
    props <- list(id=id, viewportStyle=viewportStyle, stageParameters=stageParameters, imageParameters=imageParameters, downloadImage=downloadImage, pdbString=pdbString, data=data, molStyle=molStyle)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashNgl',
        namespace = 'dash_ngl',
        propNames = c('id', 'viewportStyle', 'stageParameters', 'imageParameters', 'downloadImage', 'pdbString', 'data', 'molStyle'),
        package = 'dashNgl'
        )

    structure(component, class = c('dash_component', 'list'))
}
