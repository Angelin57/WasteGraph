class WasteGraphApp {
    constructor() {
        this.baseUrl = window.location.origin;
        this.graphData = { nodes: [], edges: [] };
        this.colors = null;
        this.selectedNode = null;
        this.shortestPath = null;
        this.init();
    }

    init() {
        this.loadGraph();
        this.setupEventListeners();
    }

    setupEventListeners() {
        const svg = document.getElementById('graphCanvas');
        svg.addEventListener('click', (e) => {
            this.handleCanvasClick(e);
        });
    }

    async loadGraph() {
        try {
            const response = await fetch(`${this.baseUrl}/graph`);
            const result = await response.json();
            
            if (result.status === 'success') {
                this.graphData = result.data;
                this.renderGraph();
                this.updateNodeSelects();
            } else {
                this.showError('Erreur lors du chargement du graphe: ' + result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion au serveur: ' + error.message);
        }
    }

    updateNodeSelects() {
        const selects = [
            'startNode', 'endNode', 'constraintNodeA', 'constraintNodeB', 'edgeU', 'edgeV'
        ];
        
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select) {
                const currentValue = select.value;
                select.innerHTML = '<option value="">Sélectionner</option>';
                
                this.graphData.nodes.forEach(node => {
                    const option = document.createElement('option');
                    option.value = node.id;
                    option.textContent = node.id;
                    select.appendChild(option);
                });
                
                if (currentValue && this.graphData.nodes.some(node => node.id === currentValue)) {
                    select.value = currentValue;
                }
            }
        });
    }

    renderGraph() {
        const svg = document.getElementById('graphCanvas');
        svg.innerHTML = '';

        // Rendre les arêtes d'abord
        this.graphData.edges.forEach(edge => {
            const uNode = this.graphData.nodes.find(n => n.id === edge.u);
            const vNode = this.graphData.nodes.find(n => n.id === edge.v);
            
            if (uNode && vNode) {
                this.renderEdge(edge, uNode, vNode);
            }
        });

        // Rendre les nœuds ensuite
        this.graphData.nodes.forEach(node => {
            this.renderNode(node);
        });
    }

    renderNode(node) {
        const svg = document.getElementById('graphCanvas');
        const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        group.classList.add('node');
        group.setAttribute('transform', `translate(${node.x}, ${node.y})`);
        group.setAttribute('data-node-id', node.id);

        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('r', '25');
        circle.setAttribute('fill', this.getNodeColor(node.id));
        circle.setAttribute('stroke', '#2c3e50');
        circle.setAttribute('stroke-width', '3');
        circle.setAttribute('cursor', 'pointer');

        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.classList.add('node-label');
        text.setAttribute('y', '5');
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('font-weight', 'bold');
        text.setAttribute('pointer-events', 'none');
        text.setAttribute('fill', 'white');
        text.setAttribute('font-size', '14');
        text.textContent = node.id;

        group.appendChild(circle);
        group.appendChild(text);
        svg.appendChild(group);
    }

    renderEdge(edge, uNode, vNode) {
        const svg = document.getElementById('graphCanvas');
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        
        line.setAttribute('x1', uNode.x);
        line.setAttribute('y1', uNode.y);
        line.setAttribute('x2', vNode.x);
        line.setAttribute('y2', vNode.y);
        
        if (this.shortestPath && this.isEdgeInPath(edge.u, edge.v)) {
            line.classList.add('path-edge');
        } else {
            line.classList.add('edge');
        }

        // Label de l'arête
        const midX = (parseFloat(uNode.x) + parseFloat(vNode.x)) / 2;
        const midY = (parseFloat(uNode.y) + parseFloat(vNode.y)) / 2;
        
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.classList.add('edge-label');
        text.setAttribute('x', midX);
        text.setAttribute('y', midY - 8);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('pointer-events', 'none');
        
        let label = `${edge.weight}`;
        if (edge.constraint_value > 0) {
            label += `+${edge.constraint_value}`;
        }
        text.textContent = label;

        svg.appendChild(line);
        svg.appendChild(text);
    }

    // Méthodes pour la gestion des sommets, arêtes, contraintes et algorithmes
    // (Ces méthodes restent identiques à la version précédente)

    async addNode() {
        const id = document.getElementById('nodeId').value;
        const x = parseFloat(document.getElementById('nodeX').value);
        const y = parseFloat(document.getElementById('nodeY').value);
        const capacity = parseInt(document.getElementById('nodeCapacity').value) || null;

        if (!id || isNaN(x) || isNaN(y)) {
            this.showError('Veuillez remplir tous les champs obligatoires pour le sommet');
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/node`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, x, y, capacity })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Sommet ajouté avec succès');
                this.clearNodeForm();
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async updateNode() {
        const id = document.getElementById('nodeId').value;
        const x = parseFloat(document.getElementById('nodeX').value);
        const y = parseFloat(document.getElementById('nodeY').value);
        const capacity = parseInt(document.getElementById('nodeCapacity').value) || null;

        if (!id) {
            this.showError('Veuillez sélectionner un sommet à modifier');
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/node`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    id, 
                    x: isNaN(x) ? null : x, 
                    y: isNaN(y) ? null : y, 
                    capacity 
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Sommet modifié avec succès');
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async deleteNode() {
        const id = document.getElementById('nodeId').value;

        if (!id) {
            this.showError('Veuillez sélectionner un sommet à supprimer');
            return;
        }

        if (!confirm(`Êtes-vous sûr de vouloir supprimer le sommet ${id} ?`)) {
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/node?id=${id}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Sommet supprimé avec succès');
                this.clearNodeForm();
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async addEdge() {
        const u = document.getElementById('edgeU').value;
        const v = document.getElementById('edgeV').value;
        const weight = parseFloat(document.getElementById('edgeWeight').value);

        if (!u || !v || isNaN(weight)) {
            this.showError('Veuillez remplir tous les champs obligatoires pour l\'arête');
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/edge`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ u, v, weight, constraint_value: 0 })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Arête ajoutée avec succès');
                this.clearEdgeForm();
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async updateEdge() {
        const u = document.getElementById('edgeU').value;
        const v = document.getElementById('edgeV').value;
        const weight = parseFloat(document.getElementById('edgeWeight').value);

        if (!u || !v) {
            this.showError('Veuillez sélectionner une arête à modifier');
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/edge`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    u, v, 
                    weight: isNaN(weight) ? null : weight 
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Arête modifiée avec succès');
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async deleteEdge() {
        const u = document.getElementById('edgeU').value;
        const v = document.getElementById('edgeV').value;

        if (!u || !v) {
            this.showError('Veuillez sélectionner une arête à supprimer');
            return;
        }

        if (!confirm(`Êtes-vous sûr de vouloir supprimer l'arête entre ${u} et ${v} ?`)) {
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/edge?u=${u}&v=${v}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Arête supprimée avec succès');
                this.clearEdgeForm();
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async addConstraint() {
        const u = document.getElementById('constraintNodeA').value;
        const v = document.getElementById('constraintNodeB').value;
        const constraintValue = parseFloat(document.getElementById('constraintValue').value);

        if (!u || !v || isNaN(constraintValue)) {
            this.showError('Veuillez sélectionner deux sommets et une valeur de contrainte');
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/edge`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    u, v, 
                    constraint_value: constraintValue 
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Contrainte ajoutée avec succès');
                document.getElementById('constraintValue').value = '';
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async removeConstraint() {
        const u = document.getElementById('constraintNodeA').value;
        const v = document.getElementById('constraintNodeB').value;

        if (!u || !v) {
            this.showError('Veuillez sélectionner deux sommets');
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/graph/edge`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    u, v, 
                    constraint_value: 0 
                })
            });

            const result = await response.json();
            
            if (result.status === 'success') {
                this.showSuccess('Contrainte supprimée avec succès');
                document.getElementById('constraintValue').value = '';
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async findShortestPath() {
        const src = document.getElementById('startNode').value;
        const dst = document.getElementById('endNode').value;

        if (!src || !dst) {
            this.showError('Veuillez sélectionner les points de départ et d\'arrivée');
            return;
        }

        try {
            const response = await fetch(`${this.baseUrl}/algo/dijkstra?src=${src}&dst=${dst}`);
            const result = await response.json();
            
            if (result.status === 'success') {
                this.shortestPath = result.data;
                this.displayResults(`Chemin: ${result.data.path.join('→')}<br>Distance: ${result.data.distance}`);
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    async colorGraph() {
        try {
            const response = await fetch(`${this.baseUrl}/algo/coloring`);
            const result = await response.json();
            
            if (result.status === 'success') {
                this.colors = result.data;
                this.showSuccess('Graphe colorié avec succès');
                this.updateColorLegend();
                this.loadGraph();
            } else {
                this.showError(result.message);
            }
        } catch (error) {
            this.showError('Erreur de connexion');
        }
    }

    updateColorLegend() {
        if (!this.colors) return;

        const legend = document.getElementById('colorLegend');
        const uniqueColors = new Map();
        
        Object.entries(this.colors).forEach(([nodeId, colorInfo]) => {
            if (!uniqueColors.has(colorInfo.color)) {
                uniqueColors.set(colorInfo.color, colorInfo.day);
            }
        });
        
        let html = '';
        uniqueColors.forEach((day, colorIndex) => {
            html += `
                <div class="legend-item">
                    <div class="color-box" style="background-color: ${this.getColor(colorIndex)}"></div>
                    <span class="legend-label">${day}</span>
                </div>
            `;
        });
        
        legend.innerHTML = html;
    }

    displayResults(content) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = `<h3>Résultats Dijkstra</h3>${content}`;
    }

    getNodeColor(nodeId) {
        if (this.colors && this.colors[nodeId]) {
            const colorIndex = this.colors[nodeId].color;
            return this.getColor(colorIndex);
        }
        return '#3498db'; // Couleur par défaut
    }

    getColor(index) {
        const colors = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
            '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
        ];
        return colors[index % colors.length];
    }

    isEdgeInPath(u, v) {
        if (!this.shortestPath) return false;
        
        const path = this.shortestPath.path;
        for (let i = 0; i < path.length - 1; i++) {
            if ((path[i] === u && path[i+1] === v) || (path[i] === v && path[i+1] === u)) {
                return true;
            }
        }
        return false;
    }

    handleCanvasClick(e) {
        const target = e.target;
        let nodeId = null;
        
        if (target.classList.contains('node')) {
            nodeId = target.getAttribute('data-node-id');
        } else if (target.tagName === 'circle') {
            nodeId = target.parentElement.getAttribute('data-node-id');
        }
        
        if (nodeId) {
            this.selectNode(nodeId);
        }
    }

    selectNode(nodeId) {
        this.selectedNode = nodeId;
        // Mettre à jour les formulaires avec les données du nœud sélectionné
        const node = this.graphData.nodes.find(n => n.id === nodeId);
        if (node) {
            document.getElementById('nodeId').value = node.id;
            document.getElementById('nodeX').value = node.x;
            document.getElementById('nodeY').value = node.y;
            document.getElementById('nodeCapacity').value = node.capacity || '';
        }
    }

    clearNodeForm() {
        document.getElementById('nodeId').value = '';
        document.getElementById('nodeX').value = '';
        document.getElementById('nodeY').value = '';
        document.getElementById('nodeCapacity').value = '';
    }

    clearEdgeForm() {
        document.getElementById('edgeWeight').value = '';
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        // Créer un message temporaire
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 5000);
    }
}

// Initialisation de l'application
const app = new WasteGraphApp();

// Fonctions globales
function addNode() { app.addNode(); }
function updateNode() { app.updateNode(); }
function deleteNode() { app.deleteNode(); }
function addEdge() { app.addEdge(); }
function updateEdge() { app.updateEdge(); }
function deleteEdge() { app.deleteEdge(); }
function addConstraint() { app.addConstraint(); }
function removeConstraint() { app.removeConstraint(); }
function findShortestPath() { app.findShortestPath(); }
function colorGraph() { app.colorGraph(); }
function loadGraph() { app.loadGraph(); }