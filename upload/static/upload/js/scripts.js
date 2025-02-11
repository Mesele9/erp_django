document.addEventListener('DOMContentLoaded', function () {
    const categoryCards = document.querySelectorAll('.category-card');
    const menuItems = document.querySelectorAll('.menu-item');
    const searchInput = document.getElementById('search-input');
    const categorySection = document.getElementById('category-section');
    const menuSection = document.getElementById('menu-section');
    const backToCategoriesBtn = document.getElementById('back-to-categories-btn');
    const showAllBtn = document.getElementById('show-all-btn');
    const noItemsMessage = document.getElementById('no-items-message');

    let currentCategoryId = null; // Track the selected category

    // Initially hide all menu items
    menuItems.forEach(item => item.style.display = 'none');

    // Function to display menu items based on category and search
    function filterMenuItems() {
        const searchQuery = searchInput.value.toLowerCase();
        let itemsFound = false;

        menuItems.forEach(item => {
            const itemName = item.querySelector('.card-title').textContent.toLowerCase();
            const itemDescription = item.querySelector('.card-text').textContent.toLowerCase();
            const itemCategoryId = item.getAttribute('data-category-id');

            const matchesSearch = itemName.includes(searchQuery) || itemDescription.includes(searchQuery);
            const matchesCategory = currentCategoryId === null || itemCategoryId === currentCategoryId;

            if (matchesSearch && matchesCategory) {
                item.style.display = 'block';
                itemsFound = true;
            } else {
                item.style.display = 'none';
            }
        });

        // Show/hide the no items message
        if (noItemsMessage) {
            noItemsMessage.style.display = itemsFound ? 'none' : 'block';
        }

        // Show menu section only if items are found
        menuSection.style.display = itemsFound ? 'block' : 'none';
    }

    // Event delegation for category cards
    document.getElementById('category-section').addEventListener('click', function (event) {
        if (event.target.closest('.category-card')) {
            const card = event.target.closest('.category-card');
            currentCategoryId = card.getAttribute('data-category-id');
            searchInput.value = ''; // Clear search when a category is selected
            filterMenuItems();
            categorySection.style.display = 'none';
            menuSection.style.display = 'block';
        }
    });

    // Event listener for the back button
    backToCategoriesBtn.addEventListener('click', function () {
        categorySection.style.display = 'block';
        menuSection.style.display = 'none';
        currentCategoryId = null;
        searchInput.value = ''; // Clear search input
    });

    // Event listener for the show all button
    showAllBtn.addEventListener('click', function () {
        currentCategoryId = null; // Reset the selected category
        searchInput.value = ''; // Clear search input
        filterMenuItems();
        menuSection.style.display = 'block'; // Ensure menu section is visible
    });

    // Event listener for search input
    searchInput.addEventListener('input', function () {
        filterMenuItems();
    });
});