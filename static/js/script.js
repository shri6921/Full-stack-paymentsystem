function addItem() {
    const itemsDiv = document.getElementById('items');
    const itemDiv = document.createElement('div');
    itemDiv.className = 'item';
    itemDiv.innerHTML = `
        <select name="items[]" onchange="calculateTotal()">
            <option value="Paneer Tikka">Paneer Tikka (₹250)</option>
            <option value="Butter Chicken">Butter Chicken (₹350)</option>
            <option value="Dal Makhani">Dal Makhani (₹200)</option>
            <option value="Naan">Naan (₹50)</option>
            <option value="Biryani">Biryani (₹300)</option>
        </select>
        <input type="number" name="quantities[]" min="1" value="1" onchange="calculateTotal()">
        <button type="button" onclick="removeItem(this)">Remove</button>
    `;
    itemsDiv.appendChild(itemDiv);
    calculateTotal();
}

function removeItem(button) {
    button.parentElement.remove();
    calculateTotal();
}

function calculateTotal() {
    const items = document.getElementsByName('items[]');
    const quantities = document.getElementsByName('quantities[]');
    const prices = {
        'Paneer Tikka': 250,
        'Butter Chicken': 350,
        'Dal Makhani': 200,
        'Naan': 50,
        'Biryani': 300
    };
    let total = 0;
    for (let i = 0; i < items.length; i++) {
        total += prices[items[i].value] * quantities[i].value;
    }
    document.getElementById('total').textContent = total;
}