$(document).ready(function() {
    $("#copy_output").click(function() {
        /* Get the text field */
        var copyText = document.getElementById("text_out");
        /* Select the text field */
        copyText.select();
        copyText.setSelectionRange(0, 99999); /* For mobile devices */
        /* Copy the text inside the text field */
        navigator.clipboard.writeText(copyText.value);

        $(document).find($("#copy_output")).attr("value", "Copied!")
        console.log("Copied!")
    });

    $("#submit").click(function() {
        $(document).find($("#submit")).attr("value", "Submitted!")
        console.log("Submitted!")
    });

    $("#settings").click(function() {
        $("#settings_modal").modal("show")
    });
    $("#close_settings").click(function() {
        $("#settings_modal").modal("hide")
    });

    $("#reset_headings").click(function() {
        $("#headings").val("AP, TIP, NOTE, AP®, Continuity and Change, Analyzing Evidence,  Causation,  Comparison")
    });
});
