function syntaxHighlight(json) {
    json = json.replace(/\\"/g,'"');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function prettyJson(id, _json){
   this.obj = (_json === undefined || _json === null)?JSON.parse($(id).html().replace('&gt;','>')):JSON.parse(_json);
   options = { 
        defaultCollapsed: false,
        editable: false,
    }

    var editor = new JsonEditor(id, this.obj, options);
    editor.load(this.obj);
}

function hideModal(id){
    id = (id  === undefined || id === null)?'#spinnerModal':id;
    $(id).modal('hide');
}

function showModal(id){
    id = (id  === undefined || id === null)?'#spinnerModal':id;
    $(id).modal('show');
}

function goto(url){
    showModal();
    window.location.href = url;
}




function run(){
    showModal();
    $("#form-query").submit();
}

function rerun(id){
    showModal();
    this.url  = "/variants/query/"+id+"/rerun";
    goto(url);
}

function apply_filter(){
    showModal();
    $("#form-queries").submit();

}

