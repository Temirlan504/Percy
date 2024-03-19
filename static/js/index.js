document.addEventListener('DOMContentLoaded', function () {
    // Get the buttons
    let forwardButton = document.getElementById('forward');
    let backwardButton = document.getElementById('backward');

    
    // Press and hold button to move forward
    forwardButton.addEventListener('touchstart', function(e) {
        e.preventDefault();
        startAction();
    });

    // Release button to stop moving forward
    forwardButton.addEventListener('touchend', function(e) {
        e.preventDefault();
        stopAction();
    });

    // Press and hold button to move backward
    backwardButton.addEventListener('touchstart', function(e) {
        e.preventDefault();
        startActionBack();
    });

    // Release button to stop moving backward
    backwardButton.addEventListener('touchend', function(e) {
        e.preventDefault();
        stopActionBack();
    });


    // Functions definitions
    function startAction() {
        fetch('/forward-start')
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.error('Error:', error));
    }

    function stopAction() {
        fetch('/forward-stop')
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.error('Error:', error));
    }

    function startActionBack() {
        fetch('/backward-start')
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.error('Error:', error));
    }

    function stopActionBack() {
        fetch('/backward-stop')
            .then(response => response.json())
            .then(data => console.log(data.message))
            .catch(error => console.error('Error:', error));
    }
});
