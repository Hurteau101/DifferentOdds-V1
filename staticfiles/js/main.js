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

function checkCheckBoxes() {
        const checkboxes = document.querySelectorAll('.row-checkbox');
        const btnBet = document.getElementById('btnBet');
        const btnCopy = document.getElementById('btnCopy');

        const isChecked = Array.from(checkboxes).some(checkbox => checkbox.checked);
        btnBet.disabled = !isChecked;
        btnCopy.disabled = !isChecked;

        document.getElementById('btnCopy').innerHTML = '<span class="bi bi-copy"></span> Copy Link';

}

document.querySelectorAll('.row-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', checkCheckBoxes);
    });

    checkCheckBoxes();

function loopCheckboxes() {
  var urlLink = "https://app.prizepicks.com/?projections=";
  var checkboxes = document.querySelectorAll('.row-checkbox')
   var firstChecked = true;

  checkboxes.forEach(function(checkbox, index) {
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
  })

  return urlLink;
}

document.getElementById('btnBet').addEventListener('click', function() {
    urlLink = loopCheckboxes();
    window.open(urlLink, '_blank').focus();
    });

document.getElementById('btnCopy').addEventListener('click', function(){
    urlLink = loopCheckboxes();
    navigator.clipboard.writeText(urlLink)
    document.getElementById('btnCopy').innerHTML = '<span class="bi bi-copy"></span> Link Copied';
});

var table;

const sportName = document.getElementById('sport_name').textContent;

$(document).ready(function() {
    // Initialize the DataTable
    table = $('#esportsTable').DataTable({
        responsive: true,
        searching: true,  // Use 'searching' instead of 'bFilter'
        lengthMenu: [[-1, 10, 25, 50], ["All", 10, 25, 50]],
        order: [[0, "desc"]],
        autoWidth: false,  // Use 'autoWidth' instead of 'bAutoWidth'
        info: true,
        ordering: true,
        language: {
            "emptyTable": `No data found in ${sportName}. Check back later. Reminder you can click 'Esports Alerts' 
            in the top right dropdown to get notified when new data is available.`,
        },
        // language: {
        //     "emptyTable": `No data found in ${sportName}. Check back later.<br>Reminder you can click 'Esports Alerts'
        //     in the top right dropdown to get notified when new data is available.`
        // },
        buttons: [
            {
                text: 'Refresh',
                action: function (e, dt, node, config) {
                    dt.ajax.reload(); // Ensure you have set up AJAX for the table if you want to reload
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

    $('#customSearch').on('keyup', function() {
        // Check if table is initialized
        if (table) {
            table.search(this.value).draw(); // Use the value from the input field to search the DataTable
        }
    });

    $('#floatingStatSelect').on('change', function() {
        var selectedStat = $(this).val();

        console.log(selectedStat);


        if (selectedStat === "All") {
            table.column(6).search('').draw();  // Clear filter when "All" is selected
        } else {

            table.column(6).search(selectedStat, true, false).draw();  // Apply exact match filter
        }
    });

    $('#floatingTeamSelect').on('change', function() {
        var selectedTeam = $(this).val();

        if (selectedTeam === "All") {
            table.column(4).search('').draw();
        }
        else {
            table.column(4).search(selectedTeam).draw();
        }
    });

});