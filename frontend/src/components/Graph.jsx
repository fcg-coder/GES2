// src/Graph.jsx

import React, { useEffect, useRef } from 'react';
import { DataSet, Network } from 'vis-network/standalone';
import 'vis-network/styles/vis-network.css'; // Импорт стилей

const Graph = () => {
    const containerRef = useRef(null);
    const networkRef = useRef(null);

    // Пример данных для узлов и рёбер
    const nodesData = [
        { id: 1, label: 'Node 1', shape: 'box', widthConstraint: { maximum: 200 } },
        { id: 2, label: 'Node 2', shape: 'box', widthConstraint: { maximum: 200 } },
        // Добавьте другие узлы по мере необходимости
    ];

    const edgesData = [
        { from: 1, to: 2 },
        // Добавьте другие рёбра по мере необходимости
    ];

    useEffect(() => {
        if (containerRef.current) {
            const nodes = new DataSet(nodesData);
            const edges = new DataSet(edgesData);
            const data = { nodes, edges };

            const options = {
                layout: {
                    hierarchical: {
                        direction: 'UD',
                        sortMethod: 'directed',
                    },
                },
                nodes: {
                    shape: 'box',
                    color: {
                        background: 'white',
                        border: 'black',
                    },
                    font: {
                        face: 'Josefin Sans',
                    },
                },
            };

            networkRef.current = new Network(containerRef.current, data, options);

            networkRef.current.on('click', function (params) {
                const nodeId = params.nodes[0];
                const node = nodes.get(nodeId);
                if (node) {
                    const goToPage = window.confirm(`Перейти на страницу ${node.label}?`);
                    if (goToPage) {
                        const connectedNodes = networkRef.current.getConnectedNodes(nodeId);
                        const numberOfChildren = connectedNodes.length;
                        console.log(`Количество дочерних элементов для узла ${nodeId}: ${numberOfChildren}`);

                        const link = document.createElement('a');
                        link.appendChild(document.createTextNode(`Перейти на страницу ${node.label}?`));
                        link.title = node.label;
                        link.href = numberOfChildren === 1 ? `/page${nodeId}/` : `/${nodeId}/`;
                        link.target = '_self';
                        link.click();
                    }
                }
            });
        }
    }, [nodesData, edgesData]);

    return (
        <div style={{ height: '100vh', backgroundColor: 'white', fontSize: '12px', fontFamily: 'Josefin Sans, sans-serif' }}>
            <h1 style={{ textAlign: 'center' }}>Hierarchical Structure of Categories, Subcategories, and Worlds on the Website</h1>
            <div ref={containerRef} style={{ width: '100%', height: '90vh' }} />
        </div>
    );
};

export default Graph;
