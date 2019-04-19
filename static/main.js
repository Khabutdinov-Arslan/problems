$('.role_selector').change(function(){
    login = $(this).attr('id');
    role = $(this).val();
    $.post('/change_role', {login: login, role: role}, function(resp){
        location.reload();
    });
})

$('#task_form').on('submit', function(e) {
    e.preventDefault();
    handler = $('#task_form').attr('action');
    data = $('#task_form').serialize();
    $.post(handler, data, function(resp){
        location.reload();
    })
});

/*$('#task_form').submit(function(event){
    event.preventDefault();
    handler = $('#task_form').attr('action');
    data = $('#task_form').serialize();
    $.post(handler, data, function(resp){
        alert(resp);
    })
    return false;
})*/