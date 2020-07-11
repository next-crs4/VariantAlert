
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

function goto(url, nomodal){
    if (nomodal === undefined) {
        showModal();
    }
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

function details(id) {
    showModal();
    this.url = "/variants/query/"+id;
    goto(url);
}

function erase(id) {
    showModal();
    this.url = "/variants/query/"+id+"/delete";
    goto(url);
}

function download(id) {
    this.url = "/variants/query/"+id+"/download";
    goto(url, 1);
}
