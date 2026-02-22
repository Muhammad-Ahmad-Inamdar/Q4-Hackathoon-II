import React from 'react';

interface SkeletonProps {
  className?: string;
}

const Skeleton = ({ className = '' }: SkeletonProps) => {
  return (
    <div
      className={`animate-pulse bg-gray-200 dark:bg-gray-700 rounded-md ${className}`}
      style={{ backgroundColor: 'rgba(156, 163, 175, 0.3)' }}
    />
  );
};

export default Skeleton;