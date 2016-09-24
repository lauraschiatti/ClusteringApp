$(function() {
  // Clear event
  $('.preview-clear').click(function(){
      $('.preview').attr("data-content","").popover('hide');
      $('.preview-filename').val("");
      $('.preview-clear').hide();
      $('.preview-input input:file').val("");
      $(".preview-input-title").text("Browse");
  });
  // Create the preview
  $(".preview-input input:file").change(function (){
      var file = this.files[0];
      var reader = new FileReader();
      // Set preview into the popover data-content
      reader.onload = function (event) {
          $(".preview-input-title").text("Cambiar");
          $(".preview-clear").show();
          $(".preview-filename").val(file.name);

           $file_content = file_get_contents(file);

          var details = '<?php echo $file_content; ?>';
          console.log(details);

      }
      reader.readAsText(file);
  });
});
