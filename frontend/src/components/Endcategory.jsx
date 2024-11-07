import React, { useEffect, useState } from 'react';

const Endcategory = ({ subcategoryId, onClose }) => {
    const [subcategoryData, setSubcategoryData] = useState(null);

    useEffect(() => {
        const fetchSubcategoryData = async () => {
            try {
                console.log('Fetching data for subcategoryId:', subcategoryId);
                const response = await fetch(`/api/${subcategoryId}`);
                const data = await response.json();
                console.log('Fetched data:', data);
                setSubcategoryData(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        // Если subcategoryId существует, выполняем запрос
        if (subcategoryId) {
            fetchSubcategoryData();
        }
    }, [subcategoryId]);

    // Если данные еще не загружены, показываем "Loading..."
    if (!subcategoryData) {
        return <div>Loading...</div>;
    }

    // Теперь данные точно есть, извлекаем их
    const { category, pages } = subcategoryData;
    const categoryName = category ? category.nameOfCategory : 'No Category Name';

    return (
        <div>
            <h2>{categoryName}</h2>
            <p>Additional information about this subcategory.</p>

            <h3>Pages:</h3>
            <ul>
                {pages && pages.length > 0 ? (
                    pages.map((page) => (
                        <li key={page.id}>
                            {page.nameOfPage}
                        </li>
                    ))
                ) : (
                    <li>No pages available.</li>
                )}
            </ul>

            <button onClick={onClose}>Close</button>
        </div>
    );
};

export default Endcategory;
