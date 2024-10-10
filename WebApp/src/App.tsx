import React, { useState } from 'react';

const App = () => {
    const [coordinates, setCoordinates] = useState({
        lowerLeft: [0, 0],
        lowerRight: [0, 0],
        upperRight: [0, 0],
        upperLeft: [0, 0],
        closing: [0, 0]
    });
    const [timeFrame, setTimeFrame] = useState('');

    const handleCoordinateChange = (corner: string, index: number, value: string) => {
        const updatedCoordinates = { ...coordinates };
        updatedCoordinates[corner][index] = parseFloat(value);
        setCoordinates(updatedCoordinates);
    };

    const handleSubmit = (event: { preventDefault: () => void; }) => {
        event.preventDefault();

        // log the coordinates for now
        console.log('Coordinates:', coordinates);

        // validate the time frame input format
        const timeFrameRegex = /^\d{4}-\d{2}-\d{2}\/\d{4}-\d{2}-\d{2}$/;
        if (!timeFrameRegex.test(timeFrame)) {
            console.error('Invalid time frame format. Please use "YYYY-MM-DD/YYYY-MM-DD".');
            return;
        }

        console.log('Time Frame:', timeFrame);
        // add logic to handle the input values here
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Time Series Forecasting of Water Quality Indices</h1>
            <form onSubmit={handleSubmit}>
                <h2>Enter the Coordinates</h2>
                <div>
                    <label>
                        Lower-left Corner:
                        <input
                            type="number"
                            value={coordinates.lowerLeft[0] || ''}
                            onChange={(e) => handleCoordinateChange('lowerLeft', 0, e.target.value)}
                            placeholder='Longitude'
                            required
                        />
                        <input
                            type="number"
                            value={coordinates.lowerLeft[1] || ''}
                            onChange={(e) => handleCoordinateChange('lowerLeft', 1, e.target.value)}
                            placeholder='Latitude'
                            required
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Lower-right Corner:
                        <input
                            type="number"
                            value={coordinates.lowerRight[0] || ''}
                            onChange={(e) => handleCoordinateChange('lowerRight', 0, e.target.value)}
                            placeholder='Longitude'
                            required
                        />
                        <input
                            type="number"
                            value={coordinates.lowerRight[1] || ''}
                            onChange={(e) => handleCoordinateChange('lowerRight', 1, e.target.value)}
                            placeholder='Latitude'
                            required
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Upper-right Corner:
                        <input
                            type="number"
                            value={coordinates.upperRight[0] || ''}
                            onChange={(e) => handleCoordinateChange('upperRight', 0, e.target.value)}
                            placeholder='Longitude'
                            required
                        />
                        <input
                            type="number"
                            value={coordinates.upperRight[1] || ''}
                            onChange={(e) => handleCoordinateChange('upperRight', 1, e.target.value)}
                            placeholder='Latitude'
                            required
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Upper-left Corner:
                        <input
                            type="number"
                            value={coordinates.upperLeft[0] || ''}
                            onChange={(e) => handleCoordinateChange('upperLeft', 0, e.target.value)}
                            placeholder='Longitude'
                            required
                        />
                        <input
                            type="number"
                            value={coordinates.upperLeft[1] || ''}
                            onChange={(e) => handleCoordinateChange('upperLeft', 1, e.target.value)}
                            placeholder='Latitude'
                            required
                        />
                    </label>
                </div>
                <div>
                    <label>
                        Closing Point:
                        <input
                            type="number"
                            value={coordinates.closing[0] || ''}
                            onChange={(e) => handleCoordinateChange('closing', 0, e.target.value)}
                            placeholder='Longitude'
                            required
                        />
                        <input
                            type="number"
                            value={coordinates.closing[1] || ''}
                            onChange={(e) => handleCoordinateChange('closing', 1, e.target.value)}
                            placeholder='Latitude'
                            required
                        />
                    </label>
                </div>
                <h2 style={{ marginTop: '20px' }}>Enter the Time Frame</h2>
                <div>
                    <label>
                        Enter the Time Frame:
                        <input
                            type="text"
                            value={timeFrame}
                            onChange={(e) => setTimeFrame(e.target.value)}
                            placeholder="e.g., 2013-06-01/2023-06-01"
                            required
                        />
                    </label>
                </div>
                <div style={{ marginTop: '10px' }}>
                    <button type="submit">Submit</button>
                </div>
            </form>
        </div>
    );
};

export default App;
