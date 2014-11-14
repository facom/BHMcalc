$("#reload").click(function() {
            jQuery.each($("iframe"), function() {
                $(this).attr({
                    src: $(this).attr("src")
                });
            });
            return false;
        });