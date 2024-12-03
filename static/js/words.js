$(function(){
    var loadForm = function(){
        let btn = $(this); 
        $.ajax({
            url: btn.attr("data-url"), 
            type: 'get', 
            dataType: 'json', 
            beforeSend: function(){
                $('#modal-word').modal("show");
            },
            success: function(data){
                $("#modal-word .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function(){
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                    $("#tabela-listar tbody").html(data.html_list);
                    $("#modal-word").modal("hide");
                }
                else{
                    $("#modal-word .modal-content").html(data.html_form);
                }
            }
        });
        return false
    };


    // ########## ADICIONAR Palavra ##########
    $("#adicionar-word").click(loadForm);
    $("#modal-word").on("submit", "#js-create-form", saveForm)
});