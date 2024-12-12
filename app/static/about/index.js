for(var i=0, len=localStorage.length; i<len; i++) {
    var key = localStorage.key(i);
    var value = localStorage[key];
    if (key.startsWith("dtw.")) {
        console.log(key + " => " + value);
        document.getElementById("localstorage").innerHTML += `
            <p>${key} => ${value}</p>
        `
    }
}
const reset_localstorage = () => {
    for(var i=0, len=localStorage.length; i<len; i++) {
        var key = localStorage.key(i);
        var value = localStorage[key];
        if (key && key.startsWith("dtw.")) {
            localStorage.removeItem(key)
        }
    }
    location.reload()
}
document.reset_localstorage = reset_localstorage
