CUDA_VISIBLE_DEVICES=0,1 python train_autodeeplab.py \
 --batch-size 2 --dataset cityscapes \
 --checkname July29_newbetas_branch  \
 --alpha_epoch 25 --filter_multiplier 4 \
 --resize 512 --crop_size 321