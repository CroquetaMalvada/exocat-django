$(function () {
  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $(".js-upload-photos").click(function () {
    $("#fileupload").attr('method','POST');
    $("#fileupload").click();
  });

  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#fileupload").fileupload({
    dataType: 'json',
    formData: {'imatges':$("#ids_imatges").val()},
//    messages : {
//      maxNumberOfFiles: 'AAA Maximum number of files exceeded',
//      acceptFileTypes: 'AAA File type not allowed',
//      maxFileSize: 'AAA File is too large',
//      minFileSize: 'AAA File is too small',
//      uploadedBytes : 'AAA Uploaded bytes exceed file size'
//    },
//    maxFileSize: 10000, // 10000 = 1mb
//    minFileSize: 1,   // in byte also
//    acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
    done: function (e, data) {
      if (data.result.is_valid) { // Si la imagen ha sido validada correctamente:
        $("#ids_imatges").val($("#ids_imatges").val()+data.result.id+",");
        $("#gallery tbody").prepend(
          "<tr><td><img width='100' src='" + data.result.url + "'></img>  "+data.result.name+"</td></tr>"
        );
      }else{
        alert(data.result.errormessage);
      }
    },
//    processfail: function(e, data){
//        console.log(e);
//        alert("error");
//    }
  });

});