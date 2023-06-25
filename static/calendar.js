document.addEventListener('DOMContentLoaded', function() {
    // Get the calendar element
    var calendar = document.getElementById('calendar');

    // Get the current date
    var currentDate = new Date();

    // Create an array of weekday names
    var weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Loop through the next 7 days
    for (var i = 0; i < 7; i++) {
        // Create a new date object for each day
        var day = new Date(currentDate.getTime() + i * 24 * 60 * 60 * 1000);

        // Get the weekday name for the current day
        var weekday = weekdays[day.getDay()];

        // Create a new div element for the day
        var dayElement = document.createElement('div');
        dayElement.classList.add('day');
        dayElement.innerText = weekday;

        // Append the day element to the calendar
        calendar.appendChild(dayElement);
    }
});
