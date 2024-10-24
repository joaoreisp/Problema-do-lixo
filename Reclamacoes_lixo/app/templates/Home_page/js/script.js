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







window.addEventListener("DOMContentLoaded", function() {
    // Recupera as reclamações armazenadas no localStorage
    const complaints = JSON.parse(localStorage.getItem("complaints")) || [];

    // Obtém o container onde as reclamações serão exibidas
    const complaintContainer = document.getElementById("complaintContainer");

    // Verifica se há reclamações
    if (complaints.length > 0) {
        // Itera sobre cada reclamação e cria um elemento para exibir
        complaints.forEach(function(complaint) {
            // Cria o container para cada post de reclamação
            const complaintPost = document.createElement("div");
            complaintPost.classList.add("complaint-post");

            // Adiciona o conteúdo da reclamação no post
            complaintPost.innerHTML = `
                <div class="complaint-header">
                    <span class="complaint-user">${complaint.user} (${complaint.role})</span>
                    <span class="complaint-location">${complaint.city} - ${complaint.neighborhood}</span>
                </div>
                <div class="complaint-sector">
                    <strong>Setor:</strong> ${complaint.sector}
                </div>
                <div class="complaint-content">
                    ${complaint.content}
                </div>
            `;

            // Adiciona o post ao container
            complaintContainer.appendChild(complaintPost);
        });
    } else {
        // Se não houver reclamações, exibe uma mensagem
        complaintContainer.innerHTML = "<p>Sem reclamações para exibir.</p>";
    }
});
