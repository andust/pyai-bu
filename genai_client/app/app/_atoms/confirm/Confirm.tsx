import React, { useState } from "react";
import Button from "../button/Button";

interface ConfirmProps {
  onConfirm: () => void;
  children: React.ReactNode;
}

const Confirm: React.FC<ConfirmProps> = ({ onConfirm, children }) => {
  const [isVisible, setIsVisible] = useState(true);

  const handleClick = () => {
    setIsVisible(false);
  };

  const handleConfirm = () => {
    onConfirm();
    setIsVisible(true);
  };

  const handleCancel = () => {
    setIsVisible(true);
  };

  return (
    <div>
      {isVisible && <span onClick={handleClick}>{children}</span>}
      {!isVisible && (
        <div className="flex items-center space-x-3">
          <p>Are you sure you want to continue?</p>
          <Button theme="danger" onClick={handleConfirm}>
            Yes
          </Button>
          <Button theme="primary" onClick={handleCancel}>
            No
          </Button>
        </div>
      )}
    </div>
  );
};

export default Confirm;
