import os
import random
from glob import glob
from pathlib import Path
import shutil

def split_dataset(
    images_dir,
    labels_dir,
    output_dir,
    train_ratio=0.8,
    val_ratio=0.1,
    test_ratio=0.1,
    copy_files=False
):
    """
    Splits the dataset into training, validation, and test sets.

    Args:
        images_dir (str): Path to the directory containing images.
        labels_dir (str): Path to the directory containing labels.
        output_dir (str): Path to the output directory where split files will be saved.
        train_ratio (float): Proportion of data to use for training.
        val_ratio (float): Proportion of data to use for validation.
        test_ratio (float): Proportion of data to use for testing.
        copy_files (bool): If True, images and labels will be copied to separate directories for each set.

    Returns:
        None
    """
    # Ensure the ratios sum to 1
    total_ratio = train_ratio + val_ratio + test_ratio
    assert abs(total_ratio - 1.0) < 1e-6, "Train, val, and test ratios must sum to 1."

    # Get list of image files
    image_extensions = ('*.jpg', '*.JPG')
    image_files = []
    for ext in image_extensions:
        image_files.extend(Path(images_dir).rglob(ext))

    # Get corresponding label files
    image_label_pairs = []
    for img_path in image_files:
        # Construct the corresponding label path
        relative_path = img_path.relative_to(images_dir)
        label_path = Path(labels_dir) / relative_path.with_suffix('.txt')

        
        image_label_pairs.append((img_path, label_path))
        
    print(f"Total image-label pairs found: {len(image_label_pairs)}")

    # Shuffle the data
    random.seed(42)  # For reproducibility
    random.shuffle(image_label_pairs)

    # Calculate split indices
    total = len(image_label_pairs)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_set = image_label_pairs[:train_end]
    val_set = image_label_pairs[train_end:val_end]
    test_set = image_label_pairs[val_end:]

    # Create output directories
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write the image paths to train.txt, val.txt, test.txt
    sets = {
        'train': train_set,
        'val': val_set,
        'test': test_set
    }

    for set_name, dataset in sets.items():
        txt_path = output_dir / f'{set_name}.txt'
        with txt_path.open('w') as f:
            for img_path, _ in dataset:
                f.write(f'{img_path.resolve()}\n')

    # Optionally, copy images and labels to separate directories
    if copy_files:
        for set_name, dataset in sets.items():
            images_dest = output_dir / 'images' / set_name
            labels_dest = output_dir / 'labels' / set_name
            images_dest.mkdir(parents=True, exist_ok=True)
            labels_dest.mkdir(parents=True, exist_ok=True)

            for img_path, lbl_path in dataset:
                # Copy images
                dest_img_path = images_dest / img_path.name
                shutil.copy(img_path, dest_img_path)

                # Copy labels
                dest_lbl_path = labels_dest / lbl_path.name
                shutil.copy(lbl_path, dest_lbl_path)

    print(f"Dataset split into {len(train_set)} training, {len(val_set)} validation, and {len(test_set)} test images.")
    print(f"Split files are saved in {output_dir}")

# Example usage:
if __name__ == '__main__':
    images_directory = 'sampled_dataset/images'
    labels_directory = 'sampled_dataset/labels'
    output_directory = 'sampled_dataset/split_files'

    split_dataset(
        images_dir=images_directory,
        labels_dir=labels_directory,
        output_dir=output_directory,
        train_ratio=0.8,
        val_ratio=0.1,
        test_ratio=0.1,
        copy_files=False  # Set to True if you want to copy files to separate directories
    )
