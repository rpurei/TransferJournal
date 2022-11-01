function delete_qr_input_row(element_id) {
    document.getElementById("input-qr-code-" + element_id).remove();
    document.getElementById("button-delete-qr-code-" + element_id).remove();
    document.getElementById("button-clear-qr-code-" + element_id).remove();
    document.getElementById("div-input-" + element_id).remove();
}

function clear_qr_input(element_id) {
    document.getElementById("input-qr-code-" + element_id).value = "";
    document.getElementById("input-qr-code-" + element_id).focus();
}

function make_input_id(length) {
    var result           = '';
    var characters       = 'abcdefghijklmnopqrstuvwxyz0123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    return result;
}

function add_qr_input(parent_div_id) {
    let element_tail = make_input_id(8);
    let parent_div = document.getElementById(parent_div_id);
    let input_element = document.createElement('input');
    let group_div = document.createElement('div');
    let input_delete_button = document.createElement('button');
    let input_clear_button = document.createElement('button');
    let input_span = document.createElement('span');

    group_div.className = "input-group mb-3";
    group_div.id = "div-input-" + element_tail;

    input_element.className = "form-control";
    input_element.id = "input-qr-code-" + element_tail;
    input_element.name = "input-qr-code-" + element_tail;
    input_element.type = "text";

    input_delete_button.className = "btn btn-outline-danger";
    input_delete_button.type = "button";
    input_delete_button.id = "button-delete-qr-code-" + element_tail;
    input_delete_button.innerHTML = "<i class=\"bi bi-trash\"></i>";
    input_delete_button.title = "Удалить запись";
    input_delete_button.onclick = function () {
        delete_qr_input_row(element_tail);
    };

    input_clear_button.className = "btn btn-outline-warning";
    input_clear_button.type = "button";
    input_clear_button.id = "button-clear-qr-code-" + element_tail;
    input_clear_button.innerHTML = "<i class=\"bi bi-x-circle\"></i>";
    input_clear_button.title = "Очистить запись";
    input_clear_button.onclick = function () {
        clear_qr_input(element_tail);
    };

    input_span.className = "input-group-text";
    input_span.innerHTML = "<i class=\"bi bi-upc-scan\"></i>";

    group_div.appendChild(input_span);
    group_div.appendChild(input_element);
    group_div.appendChild(input_clear_button);
    group_div.appendChild(input_delete_button);

    parent_div.appendChild(group_div);
    input_element.focus();
}

function add_qr_input_manual() {
    add_qr_input("qr-list");
}

$(document).ready(function(){
add_qr_input("qr-list");

$("#qr-list").on("keypress", function (event) {
    var keyPressed = event.keyCode || event.which;
    if (keyPressed === 13) {
        add_qr_input("qr-list");
        event.preventDefault();
        return false;
    }
});
});
