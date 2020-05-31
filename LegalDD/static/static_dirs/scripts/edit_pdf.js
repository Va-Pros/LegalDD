var downloadLink
var documentFrame
var selector

function init()
{
    downloadLink = document.getElementById("download")
    documentFrame = document.getElementById("doc")
    selector = document.getElementById("selDoc")
}

async function reloadDocument()
{
    var bytes = await (await fetch('/documents/' + selector.value + '/')).arrayBuffer()
    var pdfBlob = new Blob([bytes], {type: "application/pdf"})
    var fileBlob = new Blob([bytes], {type: "octet/stream"})
    documentFrame.src = window.URL.createObjectURL(pdfBlob)
    download.href = window.URL.createObjectURL(fileBlob)
    download.download = selector[selector.selectedIndex].innerText
}