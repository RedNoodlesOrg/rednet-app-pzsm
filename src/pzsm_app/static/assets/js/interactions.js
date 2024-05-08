function restart() {
    fetch('/cmd/restart', { method: 'POST' }).then(response => response.json()).then(data => show_result(data.success));
}

function apply_mods() {
    fetch('/cmd/applymods', { method: 'POST' }).then(response => response.json()).then(data => show_result(data.success));
}

function apply_checkbox(e, workshop_id, mod_id) {
  fetch(`cmd/update/mod/${ workshop_id}/${mod_id}/${e.target.checked? 1 : 0}`, { method: 'POST' })
}
function show_result(success) {
    if (success) {
        showToast("Your action was successful.", true)
    }
    else {
        showToast("There was an error performing the action.", false)
    }
}

function showToast(message, isSuccess) {
    let toastId = 'toast-' + Date.now(); // Unique ID for each toast
    let toastHtml = `
    <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header ${ isSuccess ? "bg-success" : "bg-danger"}">
      <strong class="me-auto text-white shadow">${ isSuccess ? "Success!" : "Error!" }</strong>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      ${message}
    </div>
  </div>
`;
    document.getElementById("toast-container").innerHTML += toastHtml;
    var myToastEl = document.getElementById(toastId)
    myToastEl.addEventListener('hidden.bs.toast', function () {
        myToastEl.remove()
      })
    var myToast = bootstrap.Toast.getOrCreateInstance(myToastEl)
    myToast.show()
}
