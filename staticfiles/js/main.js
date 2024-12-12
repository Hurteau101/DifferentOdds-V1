var viewportmeta = document.querySelector('meta[name="viewport"]');
if (viewportmeta) {
    if (screen.width < 425) {
        var newScale = screen.width / 425;
        viewportmeta.content = 'width=425, minimum-scale=' + newScale + ', maximum-scale=1.0, user-scalable=no, initial-scale=' + newScale + '';
    } else {
        viewportmeta.content = 'width=device-width, maximum-scale=1.0, initial-scale=1.0';
    }
}

// Convert timestamps to user's local timezone
document.querySelectorAll('td[data-timestamp]').forEach(function (cell) {
    const timestamp = parseInt(cell.getAttribute('data-timestamp')) * 1000; // Convert to milliseconds
    const localDate = new Date(timestamp);

    // Get the hour and minute
    let hours = localDate.getHours();
    const minutes = String(localDate.getMinutes()).padStart(2, '0');

    // Determine AM/PM
    const ampm = hours >= 12 ? 'PM' : 'AM';

    // Convert to 12-hour format and remove leading zero
    hours = hours % 12 || 12; // Convert to 12-hour format, 0 becomes 12

    // Get the month and day
    const options = { month: 'short' }; // Short month name (e.g., Oct)
    const month = localDate.toLocaleString('en-US', options);
    const day = localDate.getDate(); // Day of the month

    // Format the final output
    const formattedTime = `${hours}:${minutes} ${ampm} (${month}. ${day})`;
    cell.textContent = formattedTime; // Update the cell content
});

document.addEventListener('DOMContentLoaded', function () {
    function checkCheckBoxes() {
        const checkboxes = document.querySelectorAll('.row-checkbox');
        const btnBet = document.getElementById('btnBet');
        const btnCopy = document.getElementById('btnCopy');

        if (btnBet && btnCopy) {
            const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
            btnBet.disabled = !isChecked;
            btnCopy.disabled = !isChecked;
            btnCopy.innerHTML = '<span class="bi bi-copy"></span> Copy Link';
        }
    }

    function loopCheckboxes() {
        const checkboxes = document.querySelectorAll('.row-checkbox');
        const btnBet = document.getElementById('btnBet');
        const btnCopy = document.getElementById('btnCopy');

        if (btnBet && btnCopy) {
            var urlLink = "https://app.prizepicks.com/?projections=";
            var firstChecked = true;

            checkboxes.forEach(function (checkbox) {
                if (checkbox.checked) {
                    var prizepickValue = checkbox.getAttribute('data-value');
                    if (firstChecked) {
                        urlLink += prizepickValue;
                        firstChecked = false;
                    } else {
                        urlLink += "," + prizepickValue;
                    }
                }

                checkbox.checked = false;
                checkCheckBoxes();
            });

            return urlLink;
        }
    }

    document.querySelectorAll('.row-checkbox').forEach(function (checkbox) {
        checkbox.addEventListener('change', checkCheckBoxes);
    });

    checkCheckBoxes();

    const btnBet = document.getElementById('btnBet');
    const btnCopy = document.getElementById('btnCopy');

    if (btnBet) {
        btnBet.addEventListener('click', function () {
            const urlLink = loopCheckboxes();
            window.open(urlLink, '_blank').focus();
        });
    }

    if (btnCopy) {
        btnCopy.addEventListener('click', function () {
            const urlLink = loopCheckboxes();
            navigator.clipboard.writeText(urlLink);
            btnCopy.innerHTML = '<span class="bi bi-copy"></span> Link Copied';
        });
    }

    var table;
    const sportNameElement = document.getElementById('sport_name');

    if (sportNameElement) {
        const sportName = sportNameElement.textContent;

        // Initialize the DataTable
        var table = $('#esportsTable').DataTable({
            responsive: true,
            searching: true,
            lengthMenu: [[-1, 10, 25, 50], ["All", 10, 25, 50]],
            order: [[0, "desc"]],
            autoWidth: false,
            info: true,
            ordering: true,
            language: {
                "emptyTable": `No data found in ${sportName}. Check back later. Reminder you can click 'Esports Alerts' in the top right dropdown to get notified when new data is available.`,
            },
            buttons: [
                {
                    text: 'Refresh',
                    action: function (e, dt, node, config) {
                        dt.ajax.reload();
                    },
                    className: 'btn btn-primary',
                    attr: {
                        id: 'refreshButton'
                    }
                }
            ],
            dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6 topRight">>' +
                '<"row"<"col-sm-12"tr>>' +
                '<"row"<"col-sm-12 col-md-5 botLeft"i><"col-sm-12 col-md-7"p>>',
        });

        if (table.data().count() > 0) {
            $('<button type="button" id="refreshTable" class="btn btn-outline-danger btn-sm rounded-4 mb-2">' +
                '<span class="bi bi-arrow-clockwise"></span> Refresh Table</button>'
            ).appendTo('.topRight');
        }

        $('#refreshTable').on('click', function () {
            location.reload(true);
        });

        $('#customSearch').on('keyup', function () {
            if (table) {
                table.search(this.value).draw();
            }
        });

        $('#floatingStatSelect').on('change', function () {
            var selectedStat = $(this).val();
            if (selectedStat === "All") {
                table.column(6).search('').draw();
            } else {
                table.column(6).search(selectedStat, true, false).draw();
            }
        });

        $('#floatingTeamSelect').on('change', function () {
            var selectedTeam = $(this).val();
            if (selectedTeam === "All") {
                table.column(4).search('').draw();
            } else {
                table.column(4).search(selectedTeam).draw();
            }
        });
    }
});

const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded', function () {
    const messageForm = document.getElementById('messageForm');

    messageForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const message = document.getElementById('message').value;

        fetch('/admin_panel/send_message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    $('#popup').modal('hide'); // Close the modal
                } else {
                    alert('Failed to send message.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred.');
            });
    });
});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function fetchAlerts() {
    fetch('/users/get_user_alerts/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin'
    })
        .then(response => response.json())
        .then(data => {
            if (data.alerts.length > 0) {
                alertUser(data.alerts);
            }
        })
        .catch(error => {
            console.error('Error fetching alerts:', error);
        });
}

function alertUser(alerts) {
    const modal = new bootstrap.Modal(document.getElementById('popup'));
    const modalBody = document.querySelector('#popup .modal-body');
    const closeButton = document.querySelector('#popup .btn-secondary');

    // Clear previous messages
    modalBody.innerHTML = '';

    // Append each alert message to the modal body
    alerts.forEach(alert => {
        const p = document.createElement('p');
        p.textContent = alert.message;
        modalBody.appendChild(p);
    });

    modal.show();

    closeButton.onclick = function () {
        alerts.forEach(alert => acknowledgeAlert(alert.id));
        modal.hide();
    };
}

function acknowledgeAlert(alertId) {
    fetch('/users/acknowledge_alert/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin',
        body: JSON.stringify({ alert_id: alertId })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'success') {
                console.error('Error acknowledging alert:', data.message);
            }
        })
        .catch(error => {
            console.error('Error acknowledging alert:', error);
        });
}

// Fetch alerts every 30 seconds
setInterval(fetchAlerts, 30000);

// Fetch alerts on page load
fetchAlerts();












// // Convert timestamps to user's local timezone
// document.querySelectorAll('td[data-timestamp]').forEach(function (cell) {
//     const timestamp = parseInt(cell.getAttribute('data-timestamp')) * 1000; // Convert to milliseconds
//     const localDate = new Date(timestamp);
//
//     // Get the hour and minute
//     let hours = localDate.getHours();
//     const minutes = String(localDate.getMinutes()).padStart(2, '0');
//
//     // Determine AM/PM
//     const ampm = hours >= 12 ? 'PM' : 'AM';
//
//     // Convert to 12-hour format and remove leading zero
//     hours = hours % 12 || 12; // Convert to 12-hour format, 0 becomes 12
//
//     // Get the month and day
//     const options = { month: 'short' }; // Short month name (e.g., Oct)
//     const month = localDate.toLocaleString('en-US', options);
//     const day = localDate.getDate(); // Day of the month
//
//     // Format the final output
//     const formattedTime = `${hours}:${minutes} ${ampm} (${month}. ${day})`;
//     cell.textContent = formattedTime; // Update the cell content
// });
//
// function checkCheckBoxes() {
//         const checkboxes = document.querySelectorAll('.row-checkbox');
//         const btnBet = document.getElementById('btnBet');
//         const btnCopy = document.getElementById('btnCopy');
//
//         const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
//         btnBet.disabled = !isChecked;
//         btnCopy.disabled = !isChecked;
//
//         document.getElementById('btnCopy').innerHTML = '<span class="bi bi-copy"></span> Copy Link';
//
// }
//
// document.querySelectorAll('.row-checkbox').forEach(function(checkbox) {
//         checkbox.addEventListener('change', checkCheckBoxes);
//     });
//
//     checkCheckBoxes();
//
// function loopCheckboxes() {
//   var urlLink = "https://app.prizepicks.com/?projections=";
//   var checkboxes = document.querySelectorAll('.row-checkbox')
//    var firstChecked = true;
//
//   checkboxes.forEach(function(checkbox, index) {
//       if (checkbox.checked) {
//           var prizepickValue = checkbox.getAttribute('data-value');
//           if (firstChecked) {
//               urlLink += prizepickValue;
//               firstChecked = false;
//           } else {
//               urlLink += "," + prizepickValue;
//           }
//       }
//
//       checkbox.checked = false;
//       checkCheckBoxes();
//   })
//
//   return urlLink;
// }
//
// document.getElementById('btnBet').addEventListener('click', function() {
//     urlLink = loopCheckboxes();
//     window.open(urlLink, '_blank').focus();
//     });
//
// document.getElementById('btnCopy').addEventListener('click', function(){
//     urlLink = loopCheckboxes();
//     navigator.clipboard.writeText(urlLink)
//     document.getElementById('btnCopy').innerHTML = '<span class="bi bi-copy"></span> Link Copied';
// });
//
// var table;
//
// const sportName = document.getElementById('sport_name').textContent;
//
// $(document).ready(function() {
//     // Initialize the DataTable
//     table = $('#esportsTable').DataTable({
//         responsive: true,
//         searching: true,  // Use 'searching' instead of 'bFilter'
//         lengthMenu: [[-1, 10, 25, 50], ["All", 10, 25, 50]],
//         order: [[0, "desc"]],
//         autoWidth: false,  // Use 'autoWidth' instead of 'bAutoWidth'
//         info: true,
//         ordering: true,
//         language: {
//             "emptyTable": `No data found in ${sportName}. Check back later. Reminder you can click 'Esports Alerts'
//             in the top right dropdown to get notified when new data is available.`,
//         },
//         // language: {
//         //     "emptyTable": `No data found in ${sportName}. Check back later.<br>Reminder you can click 'Esports Alerts'
//         //     in the top right dropdown to get notified when new data is available.`
//         // },
//         buttons: [
//             {
//                 text: 'Refresh',
//                 action: function (e, dt, node, config) {
//                     dt.ajax.reload(); // Ensure you have set up AJAX for the table if you want to reload
//                 },
//                 className: 'btn btn-primary',
//                 attr: {
//                     id: 'refreshButton'
//                 }
//             }
//         ],
//
//         dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6 topRight">>' +
//             '<"row"<"col-sm-12"tr>>' +
//             '<"row"<"col-sm-12 col-md-5 botLeft"i><"col-sm-12 col-md-7"p>>',
//     });
//
//     if (table.data().count() > 0) {
//         $('<button type="button" id="refreshTable" class="btn btn-outline-danger btn-sm rounded-4 mb-2">' +
//             '<span class="bi bi-arrow-clockwise"></span> Refresh Table</button>'
//         ).appendTo('.topRight');
//     }
//
//     $('#refreshTable').on('click', function () {
//         location.reload(true);
//     });
//
//     $('#customSearch').on('keyup', function() {
//         // Check if table is initialized
//         if (table) {
//             table.search(this.value).draw(); // Use the value from the input field to search the DataTable
//         }
//     });
//
//     $('#floatingStatSelect').on('change', function() {
//         var selectedStat = $(this).val();
//
//         console.log(selectedStat);
//
//
//         if (selectedStat === "All") {
//             table.column(6).search('').draw();  // Clear filter when "All" is selected
//         } else {
//
//             table.column(6).search(selectedStat, true, false).draw();  // Apply exact match filter
//         }
//     });
//
//     $('#floatingTeamSelect').on('change', function() {
//         var selectedTeam = $(this).val();
//
//         if (selectedTeam === "All") {
//             table.column(4).search('').draw();
//         }
//         else {
//             table.column(4).search(selectedTeam).draw();
//         }
//     });
//
// });
//
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
//
// const csrftoken = getCookie('csrftoken');
//
// function fetchAlerts() {
//     fetch('/users/get_user_alerts/', {
//         method: 'GET',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken
//         },
//         credentials: 'same-origin'
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.alerts.length > 0) {
//             alertUser(data.alerts);
//         }
//     })
//     .catch(error => {
//         console.error('Error fetching alerts:', error);
//     });
// }
//
// function alertUser(alerts) {
//     const modal = new bootstrap.Modal(document.getElementById('popup'));
//     const modalBody = document.querySelector('#popup .modal-body');
//     const closeButton = document.querySelector('#popup .btn-secondary');
//
//     // Clear previous messages
//     modalBody.innerHTML = '';
//
//     // Append each alert message to the modal body
//     alerts.forEach(alert => {
//         const p = document.createElement('p');
//         p.textContent = alert.message;
//         modalBody.appendChild(p);
//     });
//
//     modal.show();
//
//     closeButton.onclick = function() {
//         alerts.forEach(alert => acknowledgeAlert(alert.id));
//         modal.hide();
//     };
// }
//
// function acknowledgeAlert(alertId) {
//     fetch('/users/acknowledge_alert/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrftoken
//         },
//         credentials: 'same-origin',
//         body: JSON.stringify({ alert_id: alertId })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.status !== 'success') {
//             console.error('Error acknowledging alert:', data.message);
//         }
//     })
//     .catch(error => {
//         console.error('Error acknowledging alert:', error);
//     });
// }
//
// // Fetch alerts every 30 seconds
// setInterval(fetchAlerts, 30000);
//
// // Fetch alerts on page load
// fetchAlerts();