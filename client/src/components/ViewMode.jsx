import { useEffect } from 'react';

const ViewMode = ({ mode, setMode }) => {
  useEffect(() => {
    localStorage.setItem('viewMode', mode);
  }, [mode]);

  return (
    <div className='mode'>
      <input
        class='tgl'
        id='cb5'
        type='checkbox'
        onChange={e => {
          if (e.target.checked) setMode('dark');
          else setMode('light');
        }}
        checked={mode === 'dark' ? true : false}
      />
      <label
        class='tgl-btn'
        data-tg-off='Light'
        data-tg-on='Dark'
        for='cb5'></label>
    </div>
  );
};

export default ViewMode;
