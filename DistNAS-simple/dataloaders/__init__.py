from dataloaders.datasets import cityscapes, kd, coco, combine_dbs, pascal, sbd
from torch.utils.data import DataLoader

def make_data_loader(args, **kwargs):

    if args.dataset == 'pascal':
        train_set = pascal.VOCSegmentation(args, split='train')
        val_set = pascal.VOCSegmentation(args, split='val')
        if args.use_sbd:
            sbd_train = sbd.SBDSegmentation(args, split='trainaug')
            train_set = combine_dbs.CombineDBs([train_set, sbd_train], excluded=[val_set])

        num_class = train_set.NUM_CLASSES
        train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, **kwargs)
        val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False, **kwargs)
        test_loader = None

        return train_loader, val_loader, test_loader, num_class

    elif args.dataset == 'cityscapes':
        if args.autodeeplab == 'search':
            train_set1, train_set2 = cityscapes.twoTrainSeg(args)
            num_class = train_set1.NUM_CLASSES
            train_loader1 = DataLoader(train_set1, batch_size=args.batch_size, shuffle=True, **kwargs)
            train_loader2 = DataLoader(train_set2, batch_size=args.batch_size, shuffle=True, **kwargs)
        elif args.autodeeplab == 'train':
            train_set = cityscapes.CityscapesSegmentation(args, split='train')
            num_class = train_set.NUM_CLASSES
            train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, **kwargs)
        else:
            raise Exception('autodeeplab param not set properly')

        val_set = cityscapes.CityscapesSegmentation(args, split='val')
        test_set = cityscapes.CityscapesSegmentation(args, split='test')
        val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False, **kwargs)
        test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False, **kwargs)

        if args.autodeeplab == 'search':
            return train_loader1, train_loader2, val_loader, test_loader, num_class
        elif args.autodeeplab == 'train':
            return train_loader, val_loader, test_loader, num_class


    elif args.dataset == 'coco':
        train_set = coco.COCOSegmentation(args, split='train')
        val_set = coco.COCOSegmentation(args, split='val')
        num_class = train_set.NUM_CLASSES
        train_loader = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, **kwargs)
        val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False, **kwargs)
        test_loader = None
        return train_loader, train_loader, val_loader, test_loader, num_class

    elif args.dataset == 'kd':
        train_set = kd.CityscapesSegmentation(args, split='train')
        val_set = kd.CityscapesSegmentation(args, split='val')
        test_set = kd.CityscapesSegmentation(args, split='test')
        num_class = train_set.NUM_CLASSES
        train_loader1 = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, **kwargs)
        train_loader2 = DataLoader(train_set, batch_size=args.batch_size, shuffle=True, **kwargs)
        val_loader = DataLoader(val_set, batch_size=args.batch_size, shuffle=False, **kwargs)
        test_loader = DataLoader(test_set, batch_size=args.batch_size, shuffle=False, **kwargs)

        return train_loader1, train_loader2, val_loader, test_loader, num_class
    else:
        raise NotImplementedError

