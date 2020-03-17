# AUTO GENERATED FILE - DO NOT EDIT

DashNglDashNgl <- function(id=NULL, viewportStyle=NULL, stageParameters=NULL, pdbString=NULL, data=NULL) {
    
    props <- list(id=id, viewportStyle=viewportStyle, stageParameters=stageParameters, pdbString=pdbString, data=data)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashNgl',
        namespace = 'dash_ngl',
        propNames = c('id', 'viewportStyle', 'stageParameters', 'pdbString', 'data'),
        package = 'dashNgl'
        )

    structure(component, class = c('dash_component', 'list'))
}
