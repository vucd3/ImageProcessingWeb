//Update image after clicking process
$("#process").click(function() {
    var mask_size = document.getElementById("mask_size").value;
    var sliderValue = document.getElementById("slider").value;

    $.ajax({
        url: "/perform_process/",
        method: "POST",
        data: {
            "mask_size": mask_size,
            "slider_value": sliderValue
        },
        success: function(response) {
            if (response.status == "fail"){
                alert("Please enter mask size!");
            }
            else{
                $("#img1").attr("src", "data:image/jpeg;base64," + response.image);
            }
            
        }
    });
});


//Update slider value 
$("#slider").on("input", function() {
    var sliderValue = this.value;
    $("#slider-value").text(sliderValue);
});

//Save information
$("#save").click(function() {
    $.ajax({
        url: "/save_infor/",
        method: "GET",
        success: function(data) {
            if (data.status == "success"){
                alert("Save image information succesfully!");
            }
            else if (data.status == "fail"){
                alert("Save image information fail!");
            }
            else{
                alert(data.status);
            }
        }
    });
});
