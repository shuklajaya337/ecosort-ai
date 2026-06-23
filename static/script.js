document.addEventListener('DOMContentLoaded', () => {
    const themeCheckbox = document.getElementById('checkbox');
    const body = document.body;
    const form = document.getElementById('classify-form');
    const itemInput = document.getElementById('item-input');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    const autocompleteList = document.getElementById('autocomplete-list');
    
    // Result Panel elements
    const resultPanel = document.getElementById('result-panel');
    const resItemName = document.getElementById('result-item-name');
    const resMethod = document.getElementById('classification-method');
    const resCategory = document.getElementById('result-category');
    const resBin = document.getElementById('result-bin');
    const resRecyclable = document.getElementById('result-recyclable');
    const resTips = document.getElementById('result-tips');
    const tipsBox = document.querySelector('.tips-box');

    /* --- Theme Manager --- */
    // Check local storage for theme preference
    const currentTheme = localStorage.getItem('theme') || 'dark';
    if (currentTheme === 'light') {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeCheckbox.checked = false;
    } else {
        body.classList.add('dark-theme');
        body.classList.remove('light-theme');
        themeCheckbox.checked = true;
    }

    themeCheckbox.addEventListener('change', () => {
        if (themeCheckbox.checked) {
            body.classList.remove('light-theme');
            body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark');
        } else {
            body.classList.remove('dark-theme');
            body.classList.add('light-theme');
            localStorage.setItem('theme', 'light');
        }
    });

    /* --- Live Autocomplete --- */
    let currentFocus = -1;

    itemInput.addEventListener('input', async (e) => {
        const query = e.target.value.trim();
        closeAllLists();
        
        if (!query) return;

        try {
            const response = await fetch(`/autocomplete?q=${encodeURIComponent(query)}`);
            const suggestions = await response.json();
            
            if (suggestions.length === 0) return;

            suggestions.forEach(item => {
                const div = document.createElement('div');
                div.className = 'autocomplete-item';
                // Highlight the matching part
                const matchIdx = item.toLowerCase().indexOf(query.toLowerCase());
                if (matchIdx !== -1) {
                    div.innerHTML = item.substr(0, matchIdx) + 
                                    "<strong>" + item.substr(matchIdx, query.length) + "</strong>" + 
                                    item.substr(matchIdx + query.length);
                } else {
                    div.textContent = item;
                }
                
                div.addEventListener('click', () => {
                    itemInput.value = item;
                    closeAllLists();
                    form.dispatchEvent(new Event('submit')); // Trigger form submission
                });
                autocompleteList.appendChild(div);
            });
        } catch (error) {
            console.error('Autocomplete fetch error:', error);
        }
    });

    // Keyboard navigation in suggestions
    itemInput.addEventListener('keydown', (e) => {
        let x = autocompleteList.getElementsByClassName('autocomplete-item');
        if (e.keyCode === 40) { // DOWN arrow
            currentFocus++;
            addActive(x);
        } else if (e.keyCode === 38) { // UP arrow
            currentFocus--;
            addActive(x);
        } else if (e.keyCode === 13) { // ENTER
            if (currentFocus > -1) {
                e.preventDefault();
                if (x[currentFocus]) {
                    x[currentFocus].click();
                }
            }
        }
    });

    function addActive(x) {
        if (!x) return false;
        removeActive(x);
        if (currentFocus >= x.length) currentFocus = 0;
        if (currentFocus < 0) currentFocus = (x.length - 1);
        x[currentFocus].classList.add('autocomplete-active');
        x[currentFocus].style.backgroundColor = 'var(--primary-glow)';
    }

    function removeActive(x) {
        for (let i = 0; i < x.length; i++) {
            x[i].classList.remove('autocomplete-active');
            x[i].style.backgroundColor = '';
        }
    }

    function closeAllLists() {
        autocompleteList.innerHTML = '';
        currentFocus = -1;
    }

    // Close dropdown when clicking outside
    document.addEventListener('click', (e) => {
        if (e.target !== itemInput) {
            closeAllLists();
        }
    });

    /* --- Form Submission & Classification --- */
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const itemVal = itemInput.value.trim();
        if (!itemVal) return;

        // Visual states: loading spinner
        btnText.style.display = 'none';
        spinner.style.display = 'inline-block';
        submitBtn.disabled = true;
        closeAllLists();

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ item: itemVal })
            });

            const result = await response.json();
            
            if (response.ok) {
                // Populate results
                resItemName.textContent = result.item;
                resMethod.textContent = result.method;
                resCategory.textContent = result.category;
                resCategory.style.color = result.color;
                
                resBin.textContent = result.bin;
                resRecyclable.textContent = result.recyclable;
                resTips.textContent = result.tips;

                // Color-code the tips border and header
                tipsBox.style.borderLeftColor = result.color;
                const tipsHeader = tipsBox.querySelector('h4');
                if (tipsHeader) tipsHeader.style.color = result.color;

                // Color-code indicators
                if (result.recyclable.toLowerCase().includes('yes')) {
                    resRecyclable.style.color = 'var(--primary)';
                } else if (result.recyclable.toLowerCase().includes('no')) {
                    resRecyclable.style.color = 'var(--hazardous)';
                } else {
                    resRecyclable.style.color = 'var(--paper)';
                }

                // Show result panel with transition
                resultPanel.style.display = 'block';
                resultPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                alert(result.error || 'Something went wrong during classification.');
            }
        } catch (error) {
            console.error('Classification error:', error);
            alert('Failed to connect to the classification server.');
        } finally {
            // Restore button visual state
            btnText.style.display = 'inline';
            spinner.style.display = 'none';
            submitBtn.disabled = false;
        }
    });
});
