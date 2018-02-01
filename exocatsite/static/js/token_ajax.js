//esta config de abajo sirve para que django con responda con un forbidden a las peticiones ajax(es el equivalente a un { csrf_token } dentro del form html
//requiere del plugin js-cookie-master!!!
var csrftoken = Cookies.get('csrftoken')


$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}