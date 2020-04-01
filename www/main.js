function myFunction()
  {
    $('#playlist').empty()
    $.ajax({
            type: "GET",
            url: "/cgi-bin/showPlaylists.py",
            success: function(data){
                console.log(data)
                // Parse the returned json data
                //var opts = $.parseJSON(data);
                // Use jQuery's each to iterate over the opts value
                $.each(data.playlists, function(i, d) {
                    // console.log(d);
                    // You will need to alter the below to get the right values from your json object.  Guessing that d.id / d.modelName are columns in your carModels data
                    $('#playlist').append('<option value="' + d + '">' + d + '</option>');
                });
            }
        });
  }

window.onload = myFunction()