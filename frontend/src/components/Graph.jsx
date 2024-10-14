import React, { useEffect, useRef, useState } from 'react';
import { DataSet, Network } from 'vis-network/standalone';
import 'vis-network/styles/vis-network.css'; // Импорт стилей

const Graph = () => {
    const containerRef = useRef(null);
    const networkRef = useRef(null);
    const [graphData, setGraphData] = useState({ nodes: [], edges: [] });

    useEffect(() => {
        // Функция для загрузки данных с сервера
        const fetchData = async () => {
            try {
                const response = await fetch('/api/graph/');
                const data = await response.json();
                setGraphData(data);
            } catch (error) {
                console.error('Error fetching graph data:', error);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        if (containerRef.current && graphData.nodes.length > 0) {
            const nodes = new DataSet(graphData.nodes);
            const edges = new DataSet(graphData.edges);
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
    }, [graphData]);

    return (
        <div style={{ height: '100vh', backgroundColor: 'white', fontSize: '12px', fontFamily: 'Josefin Sans, sans-serif' }}>
            <h1 style={{ textAlign: 'center' }}>Hierarchical Structure of Categories, Subcategories, and Worlds on the Website</h1>
            <div ref={containerRef} style={{ width: '100%', height: '90vh' }} />
        </div>
    );
};

export default Graph;
