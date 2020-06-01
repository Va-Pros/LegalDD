var downloadLink
var documentFrame
var selector
var notFound

function init()
{
    downloadLink = document.getElementById("download")
    documentFrame = document.getElementById("doc")
    selector = document.getElementById("selDoc")
    notFound = document.getElementById("notFound")
}

async function updateNotFound()
{
    var data = await (await fetch('/getstrings/' + selector.value + '/')).text()
    var notFoundStrs = JSON.parse(data)
    notFound.innerHTML = "Не были найдены ни в одном документе:<br/>"
    notFoundStrs.forEach(function(value) {
        var entry = document.createElement("p")
        entry.innerText = value
        notFound.appendChild(entry)
    })
    notFound.style.visibility = "visible"
}

async function reloadDocument()
{
    var bytes = await (await fetch('/documents/' + selector.value + '/')).arrayBuffer()
    try
    {
        var text = new TextDecoder().decode(bytes)
        if (text[0] != '<')
            throw exception
        var htmlBlob = new Blob([bytes], {type: "text/html"})
        documentFrame.src = window.URL.createObjectURL(htmlBlob)
        notFound.style.visibility = "hidden"
        return
    }
    catch
    {
        var pdfBlob = new Blob([bytes], {type: "application/pdf"})
        var fileBlob = new Blob([bytes], {type: "octet/stream"})
        documentFrame.src = window.URL.createObjectURL(pdfBlob)
        download.href = window.URL.createObjectURL(fileBlob)
        download.download = selector[selector.selectedIndex].innerText
        updateNotFound()
    }
}