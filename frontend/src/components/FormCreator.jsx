import React, { useState } from 'react';

const getRandomCoordinates = (numPoints, radius, variation) => {
    let coordinates = [];
    for (let i = 0; i < numPoints; i++) {
        const angle = (i / numPoints) * 2 * Math.PI;
        const radialOffset = radius + (Math.random() - 0.5) * variation;
        const x = 50 + radialOffset * Math.cos(angle);
        const y = 50 + radialOffset * Math.sin(angle);
        coordinates.push({ x, y });
    }
    return coordinates;
};

const generatePathData = (coordinates) => {
    let pathData = `M${coordinates[0].x},${coordinates[0].y} `;
    for (let i = 1; i < coordinates.length; i++) {
        pathData += `L${coordinates[i].x},${coordinates[i].y} `;
    }
    pathData += 'Z';
    return pathData;
};

const Blob = ({ onClick }) => {
    const radius = 40;
    const variation = 20;
    const coordinates = getRandomCoordinates(100, radius, variation);
    const pathData = generatePathData(coordinates);

    return (
        <svg width="200" height="200" viewBox="0 0 100 100" style={{ cursor: 'pointer', height: '100px' }}>
            <path d={pathData} fill="blue" stroke="black" strokeWidth="2" onClick={onClick} />
        </svg>
    );
};

const FormDistributor = ({ onFormClick }) => {
    const generateRandomPosition = () => ({
        x: Math.random() * 800,
        y: Math.random() * 600,
    });

    const numForms = 5;
    const numPoints = 100;
    const numComponents = 5;

    const handleClick = () => {
        if (typeof onFormClick === 'function') {
            onFormClick();
        }
    };

    return (
        <div style={{ height: '100%' }}>
            {[...Array(numForms)].map((_, index) => {
                const { x, y } = generateRandomPosition();
                return (
                    <div key={index} style={{ position: 'absolute', left: x, top: y }}>
                        <Blob numPoints={numPoints} numComponents={numComponents} onClick={handleClick} />
                    </div>
                );
            })}
        </div>
    );
};

const PageHome = () => {
    const [key, setKey] = useState(0);

    const handleClick = () => {
        setKey(prevKey => prevKey + 1);
        alert('Blob clicked!');
    };

    return (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
            <div style={{ flex: '1 0 auto', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <Blob onClick={handleClick} />
            </div>
        </div>
    );
};

export default PageHome;
