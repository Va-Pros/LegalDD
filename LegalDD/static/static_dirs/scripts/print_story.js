let text = "";
for(let i=0; i<localStorage.length; i++) {
    let key = localStorage.key(i + 1);
    text += localStorage.getItem(key);
}
document.getElementById('story_text').innerHTML = text;