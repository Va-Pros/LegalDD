var phraseCnt

function init(docCnt)
{
    phraseCnt = new Array(docCnt + 1).fill(0)
}

function addPhrase(index)
{
    var phrases = document.getElementById(index + "_phrases")
    var newItem = document.createElement("input")
    newItem.name = newItem.id = index + "_phrase" + phraseCnt[index]
    newItem.required = true
    phrases.appendChild(newItem)
    
    var removeNewItem = document.createElement("button")
    removeNewItem.type = "button"
    removeNewItem.innerText = "X"
    removeNewItem.class = "button"
    phrases.appendChild(removeNewItem)
    
    var newLine = document.createElement("br")
    phrases.appendChild(newLine)
    
    removeNewItem.onclick = function()
    {
        newItem.remove()
        removeNewItem.remove()
        newLine.remove()
        var currElemInd = +newItem.name.slice(-1)
        for (var ind = currElemInd + 1; ind < phraseCnt[index]; ++ind)
        {
            var input = document.getElementById(index + "_phrase" + ind)
            input.name = input.id = index + "_phrase" + (ind - 1)
        }
        document.getElementById(index + "_phraseCnt").value = --phraseCnt[index];
    }
    document.getElementById(index + "_phraseCnt").value = ++phraseCnt[index]
}