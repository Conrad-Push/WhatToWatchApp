import React from "react";

function InfoModal(props) {
  const { action, time, closeModal } = props;

  return (
    <div className="modal">
      <div className="modal-content">
        <h2>Action Successful</h2>
        <p>
          {action} action needed: {time} to complete.
        </p>
        <button onClick={closeModal}>Close</button>
      </div>
    </div>
  );
}

export default InfoModal;
