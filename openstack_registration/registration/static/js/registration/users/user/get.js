/*
Javascript module to manage all user related interaction with openstack-registration.
*/

/* getUserAttributes get information for the logged user. If there are more than one response or the
response is empty, then there are a problem */
function getUserAttributes() {
    $.getJSON(location.pahtname, {format: 'json'}
    ).done(
        function (users) {
            $('#username-info').text(users[0].uid);
            $('#email-info').text(users[0].mail);
            $('#firstname-info').text(users[0].firstname);
            $('#lastname-info').text(users[0].lastname);
        }
    );
}
