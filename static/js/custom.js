// Jquery
$(document).ready(function() {
    // DASHBOARD auto date range (monthly)
    var currentDate = new Date();
    var firstDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    var lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);

    $('.input-daterange').datepicker({
        startDate: firstDayOfMonth,
        endDate: lastDayOfMonth,
        autoclose: true,
        format: 'yyyy-mm-dd'
    });

    $('[name="auto_start_date"]').datepicker('setDate', firstDayOfMonth);
    $('[name="auto_end_date"]').datepicker('setDate', lastDayOfMonth);
    // End DASHBOARD auto date range (monthly)
    
});


// Vanilla JavaScript

// Show Alert
function showCustomAlert(message, alertType) {
    var alertClass = "";
  
    // Determine the alert class based on the alertType parameter
    if (alertType === "success") {
      alertClass = "alert-success";
    } else if (alertType === "info") {
      alertClass = "alert-info";
    } else if (alertType === "warning") {
      alertClass = "alert-warning";
    } else if (alertType === "danger") {
      alertClass = "alert-danger";
    }
  
    // Create the alert HTML dynamically
    var alertHTML = '<div class="alert ' + alertClass + ' alert-dismissible fade show custom-alert mt-2 end-0" role="alert">' +
      message +
      '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
      '<span aria-hidden="true">&times;</span>' +
      '</button>' +
      '</div>';
  
    // Append the alert HTML to the body
    $("#content-wrapper").append(alertHTML);
  
    // Hide the alert after 3 seconds
    setTimeout(function() {
      $(".custom-alert").alert("close");
    }, 4000);
}

// Show loading screen
function showLoadingScreen() {
  document.getElementById('loading-overlay').style.display = 'block';
}
// Function to hide the loading animation
function hideLoadingScreen() {
  // window.addEventListener("load", function() {
    // setTimeout(function() {
      document.getElementById('loading-overlay').style.display = 'none';
    // }, 4000);
  // });
}
// Add event listeners for page reload/redirect
window.addEventListener('beforeunload', showLoadingScreen);
document.addEventListener('DOMContentLoaded', hideLoadingScreen);

// data listing table
$('.sortable-column').click(function() {
  const sortType = $(this).data('sort');
  const arrowIcon = $(this).find('i');

  // Toggle arrow direction
  arrowIcon.toggleClass('fa-arrow-down fa-arrow-up');

  // Get the table rows for sorting
  const table = $(this).closest('table');
  const tbody = table.find('tbody');
  const rows = tbody.find('tr').get();

  // Determine the sorting order
  const sortOrder = arrowIcon.hasClass('fa-arrow-up') ? 1 : -1;

  // Sort the rows based on the data-sort attribute
  rows.sort(function(a, b) {
      const valueA = $(a).find(`[data-${sortType}]`).data(sortType);
      const valueB = $(b).find(`[data-${sortType}]`).data(sortType);

      return (valueA > valueB ? 1 : -1) * sortOrder;
  });
  tbody.empty();

  // Append sorted rows to tbody
  $.each(rows, function(index, row) {
      tbody.append(row);
  });
});