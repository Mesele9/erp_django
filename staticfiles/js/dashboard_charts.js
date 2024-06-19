document.addEventListener('DOMContentLoaded', function() {
    // Get context and data for department chart
    var departmentCtx = document.getElementById('departmentChart').getContext('2d');
    var departmentLabels = [];
    var departmentCounts = [];
    {% for data in department_data %}
        departmentLabels.push("{{ data.department__name }}");
        departmentCounts.push({{ data.employee_count }});
    {% endfor %}

    // Create department chart
    var departmentChart = new Chart(departmentCtx, {
        type: 'pie',
        data: {
            labels: departmentLabels,
            datasets: [{
                label: 'Employees by Department',
                data: departmentCounts,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    // ... other colors ...
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    // ... other colors ...
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });

    // Get context and data for gender chart
    var genderCtx = document.getElementById('genderChart').getContext('2d');
    var genderLabels = ['Male', 'Female'];
    var genderCounts = [{{ male_count }}, {{ female_count }}];

    // Create gender chart
    var genderChart = new Chart(genderCtx, {
        type: 'pie',
        data: {
            labels: genderLabels,
            datasets: [{
                label: 'Employees by Gender',
                data: genderCounts,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true
        }
    });
});