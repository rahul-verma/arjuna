function openModal(event){
    var source = event.target || event.srcElement;
    var modal = document.getElementById("modal-packet");
    modal.style.display = "block";
    var req = document.getElementById("modal-packet-request");
    req.innerHTML = ""
    var h3_req = document.createElement("h3");
    h3_req.innerHTML = "Request"
    req.appendChild(h3_req)
    req.appendChild(document.createTextNode(source.getAttribute("data-request")))

    var res = document.getElementById("modal-packet-response");
    res.innerHTML = ""
    var h3_res = document.createElement("h3");
    h3_res.innerHTML = "Response"
    req.appendChild(h3_res)
    res.appendChild(document.createTextNode(source.getAttribute("data-response")))
    var span = document.getElementById(source.id + "modal-packet-span");
    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

}

function openModalImage(event){
    var img_link = event.target || event.srcElement;
    var modal = document.getElementById("modal-image");
    var modal_image = document.getElementById("modal-image-content");
    modal.style.display = "block";
    modal_image.src = img_link.src;
    var span = document.getElementById("modal-image-span");
    span.onclick = function() {
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}


// Overriding the pytest-html's init()

function init () {
    reset_sort_headers();

    add_collapse();

    show_filters();

    sort_column(find('.initial-sort'));

    find_all('.sortable').forEach(function(elem) {
        elem.addEventListener("click",
                              function(event) {
                                  sort_column(elem);
                              }, false)
    });

    var all_redirs = document.getElementsByClassName('redir');
    Array.from(all_redirs).forEach(function(item){
        item.style.display = 'none';
    })
    find_all('.expand').forEach(function(elem) {
        elem.addEventListener("click",
            function(event) {
                var list = elem.parentElement.parentElement.parentElement.getElementsByClassName('redir');
                Array.from(list).forEach(function(item){
                    if (item.style.display == 'none'){
                        item.style.display = '';
                    } else {
                        item.style.display = 'none';
                    }
                })
        }, false)
    });
};