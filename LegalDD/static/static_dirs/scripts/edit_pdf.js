//const { PDFDocument, StandardFonts, rgb } = PDFLib

var pdfDocument;    // Сам документ

async function setDocument(docUrl)
{
    var bytes = await (await fetch(docUrl)).arrayBuffer()
    var blob = new Blob([bytes], {type: "application/pdf"});
    document.getElementById("doc").src = window.URL.createObjectURL(blob);
}

// Загрузка документа
async function construct(docUrl)
{
    const bytes = await (await fetch(docUrl)).arrayBuffer()

    pdfDocument = await PDFDocument.load(bytes)
    
    redraw()
}

// Переотрисовка
async function redraw()
{
    const pdfBytes = await pdfDocument.save();
    var blob = new Blob([pdfBytes], {type: "application/pdf"});
    var link = window.URL.createObjectURL(blob);
    document.getElementById("doc").src = link
}

var _PDF_DOC,
    _CURRENT_PAGE,
    _TOTAL_PAGES,
    _CANVAS;

// initialize and load the PDF
async function showPDF(pdf_url) {

    _CANVAS = document.getElementById('doc')

    // get handle of pdf document
    try {
        _PDF_DOC = await pdfjsLib.getDocument({ url: pdf_url });
    }
    catch(error) {
        alert(error.message);
    }

    // total pages in pdf
    _TOTAL_PAGES = _PDF_DOC.numPages;

    // show the first page
    showPage(1);
}

// load and render specific page of the PDF
async function showPage(page_no) {
    _CURRENT_PAGE = page_no;
    
    // get handle of page
    try {
        var page = await _PDF_DOC.getPage(page_no);
    }
    catch(error) {
        alert(error.message);
    }

    // original width of the pdf page at scale 1
    var pdf_original_width = page.getViewport(1).width;
    
    // as the canvas is of a fixed width we need to adjust the scale of the viewport where page is rendered
    var scale_required = _CANVAS.width / pdf_original_width;

    // get viewport to render the page at required scale
    var viewport = page.getViewport(scale_required);

    // set canvas height same as viewport height
    _CANVAS.height = viewport.height;

    // page is rendered on <canvas> element
    var render_context = {
        canvasContext: _CANVAS.getContext('2d'),
        viewport: viewport
    };
        
    // render the page contents in the canvas
    try {
        await page.render(render_context);
    }
    catch(error) {
        alert(error.message);
    }
}