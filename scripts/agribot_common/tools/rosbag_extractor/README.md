For PointClouds with intensity: there's a workaround feature, 
extractor exports only XYZ_RGB PointClouds, so intensity has been implemented
as equal values for R, B, and G. This is because open3D does not support PointClouds XYZ-I.
https://github.com/isl-org/Open3D/issues/125 