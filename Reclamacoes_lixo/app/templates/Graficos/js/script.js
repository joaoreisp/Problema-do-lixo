// Exibir o popup e o fundo preto ao clicar no ícone
document.getElementById('notification-icon').addEventListener('click', function(event) {
    event.preventDefault(); // Prevenir o comportamento padrão do link

    // Exibir o overlay com o popup
    document.getElementById('notification-overlay').style.display = 'flex';
});

// Fechar o popup ao clicar no botão "Fechar"
document.getElementById('close-popup').addEventListener('click', function() {
    document.getElementById('notification-overlay').style.display = 'none';
});
