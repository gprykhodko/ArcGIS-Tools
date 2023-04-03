########################################################################################
# Tool Name: Mapping Value Check
# Version: 
# Use: 
#      
#      
# Input parameters:  
#                    
#                   
# Author: Gennadii Prykhodko, Halff Accociates, Inc., 2022
########################################################################################
import arcpy, os, zipfile
import pandas as pd
import numpy as np
from arcgis.gis import GIS
arcpy.env.overwriteOutput = True
arcpy.env.addOutputsToMap = False
outsym = """{
  "type" : "CIMLayerDocument",
  "version" : "2.9.0",
  "build" : 32739,
  "layers" : [
    "CIMPATH=tool_3/bfe_2d_point_projectx.xml"
  ],
  "layerDefinitions" : [
    {
      "type" : "CIMFeatureLayer",
      "name" : "BFE_2D_Point_ProjectX",
      "uRI" : "CIMPATH=tool_3/bfe_2d_point_projectx.xml",
      "sourceModifiedTime" : {
        "type" : "TimeInstant"
      },
      "useSourceMetadata" : true,
      "description" : "BFE_2D_Point_ProjectX",
      "layerElevation" : {
        "type" : "CIMLayerElevationSurface",
        "mapElevationID" : "{DE120E67-7AF3-4B4B-AE34-225EE7E70F22}"
      },
      "expanded" : true,
      "layerType" : "Operational",
      "showLegends" : true,
      "visibility" : true,
      "displayCacheType" : "Permanent",
      "maxDisplayCacheAge" : 5,
      "showPopups" : true,
      "serviceLayerID" : -1,
      "refreshRate" : -1,
      "refreshRateUnit" : "esriTimeUnitsSeconds",
      "blendingMode" : "Alpha",
      "allowDrapingOnIntegratedMesh" : true,
      "autoGenerateFeatureTemplates" : true,
      "featureElevationExpression" : "0",
      "featureTable" : {
        "type" : "CIMFeatureTable",
        "displayField" : "EST_ID",
        "editable" : true,
        "fieldDescriptions" : [
          {
            "type" : "CIMFieldDescription",
            "alias" : "BFE_BASE",
            "fieldName" : "BFE_BASE",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "BLELEV1PCT",
            "fieldName" : "BLELEV1PCT",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 0
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "OBJECTID",
            "fieldName" : "OBJECTID",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 0
            },
            "readOnly" : true,
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "SHAPE",
            "fieldName" : "SHAPE",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "EST_ID",
            "fieldName" : "EST_ID",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "VERSION_ID",
            "fieldName" : "VERSION_ID",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "EBFE_LN_ID",
            "fieldName" : "EBFE_LN_ID",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "BFE_LN_TYP",
            "fieldName" : "BFE_LN_TYP",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "LEN_UNIT",
            "fieldName" : "LEN_UNIT",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "V_DATUM",
            "fieldName" : "V_DATUM",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "SOURCE_CIT",
            "fieldName" : "SOURCE_CIT",
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "Y_LAST",
            "fieldName" : "Y_LAST",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "LEN_FT",
            "fieldName" : "LEN_FT",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "X",
            "fieldName" : "X",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "Y",
            "fieldName" : "Y",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "X_FIRST",
            "fieldName" : "X_FIRST",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "Y_FIRST",
            "fieldName" : "Y_FIRST",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          },
          {
            "type" : "CIMFieldDescription",
            "alias" : "X_LAST",
            "fieldName" : "X_LAST",
            "numberFormat" : {
              "type" : "CIMNumericFormat",
              "alignmentOption" : "esriAlignRight",
              "alignmentWidth" : 0,
              "roundingOption" : "esriRoundNumberOfDecimals",
              "roundingValue" : 6
            },
            "visible" : true,
            "searchMode" : "Exact"
          }
        ],
        "dataConnection" : {
          "type" : "CIMStandardDataConnection",
          "workspaceConnectionString" : "DATABASE=.\\BLE-QAQC-Tools.gdb",
          "workspaceFactory" : "FileGDB",
          "dataset" : "BFE_2D_Point_ProjectX",
          "datasetType" : "esriDTFeatureClass"
        },
        "studyAreaSpatialRel" : "esriSpatialRelUndefined",
        "searchOrder" : "esriSearchOrderSpatial"
      },
      "featureTemplates" : [
        {
          "type" : "CIMFeatureTemplate",
          "name" : "BFE_2D_Point_ProjectX",
          "tags" : "Point",
          "toolProgID" : "2a8b3331-5238-4025-972e-452a69535b06"
        }
      ],
      "htmlPopupEnabled" : true,
      "selectable" : true,
      "featureCacheType" : "Session",
      "displayFiltersType" : "ByScale",
      "featureBlendingMode" : "Alpha",
      "labelClasses" : [
        {
          "type" : "CIMLabelClass",
          "expressionTitle" : "Custom",
          "expression" : "$feature.EST_ID",
          "expressionEngine" : "Arcade",
          "featuresToLabel" : "AllVisibleFeatures",
          "maplexLabelPlacementProperties" : {
            "type" : "CIMMaplexLabelPlacementProperties",
            "featureType" : "Point",
            "avoidPolygonHoles" : true,
            "canOverrunFeature" : true,
            "canPlaceLabelOutsidePolygon" : true,
            "canRemoveOverlappingLabel" : true,
            "canStackLabel" : true,
            "connectionType" : "Unambiguous",
            "constrainOffset" : "NoConstraint",
            "contourAlignmentType" : "Page",
            "contourLadderType" : "Straight",
            "contourMaximumAngle" : 90,
            "enableConnection" : true,
            "enablePointPlacementPriorities" : true,
            "featureWeight" : 0,
            "fontHeightReductionLimit" : 4,
            "fontHeightReductionStep" : 0.5,
            "fontWidthReductionLimit" : 90,
            "fontWidthReductionStep" : 5,
            "graticuleAlignmentType" : "Straight",
            "keyNumberGroupName" : "Default",
            "labelBuffer" : 15,
            "labelLargestPolygon" : true,
            "labelPriority" : -1,
            "labelStackingProperties" : {
              "type" : "CIMMaplexLabelStackingProperties",
              "stackAlignment" : "ChooseBest",
              "maximumNumberOfLines" : 3,
              "minimumNumberOfCharsPerLine" : 3,
              "maximumNumberOfCharsPerLine" : 24,
              "separators" : [
                {
                  "type" : "CIMMaplexStackingSeparator",
                  "separator" : " ",
                  "splitAfter" : true
                },
                {
                  "type" : "CIMMaplexStackingSeparator",
                  "separator" : ",",
                  "visible" : true,
                  "splitAfter" : true
                }
              ],
              "trimStackingSeparators" : true
            },
            "lineFeatureType" : "General",
            "linePlacementMethod" : "OffsetCurvedFromLine",
            "maximumLabelOverrun" : 36,
            "maximumLabelOverrunUnit" : "Point",
            "minimumFeatureSizeUnit" : "Map",
            "multiPartOption" : "OneLabelPerPart",
            "offsetAlongLineProperties" : {
              "type" : "CIMMaplexOffsetAlongLineProperties",
              "placementMethod" : "BestPositionAlongLine",
              "labelAnchorPoint" : "CenterOfLabel",
              "distanceUnit" : "Percentage",
              "useLineDirection" : true
            },
            "pointExternalZonePriorities" : {
              "type" : "CIMMaplexExternalZonePriorities",
              "aboveLeft" : 4,
              "aboveCenter" : 2,
              "aboveRight" : 1,
              "centerRight" : 3,
              "belowRight" : 5,
              "belowCenter" : 7,
              "belowLeft" : 8,
              "centerLeft" : 6
            },
            "pointPlacementMethod" : "AroundPoint",
            "polygonAnchorPointType" : "GeometricCenter",
            "polygonBoundaryWeight" : 0,
            "polygonExternalZones" : {
              "type" : "CIMMaplexExternalZonePriorities",
              "aboveLeft" : 4,
              "aboveCenter" : 2,
              "aboveRight" : 1,
              "centerRight" : 3,
              "belowRight" : 5,
              "belowCenter" : 7,
              "belowLeft" : 8,
              "centerLeft" : 6
            },
            "polygonFeatureType" : "General",
            "polygonInternalZones" : {
              "type" : "CIMMaplexInternalZonePriorities",
              "center" : 1
            },
            "polygonPlacementMethod" : "CurvedInPolygon",
            "primaryOffset" : 1,
            "primaryOffsetUnit" : "Point",
            "removeExtraWhiteSpace" : true,
            "repetitionIntervalUnit" : "Point",
            "rotationProperties" : {
              "type" : "CIMMaplexRotationProperties",
              "rotationType" : "Arithmetic",
              "alignmentType" : "Straight"
            },
            "secondaryOffset" : 100,
            "strategyPriorities" : {
              "type" : "CIMMaplexStrategyPriorities",
              "stacking" : 1,
              "overrun" : 2,
              "fontCompression" : 3,
              "fontReduction" : 4,
              "abbreviation" : 5
            },
            "thinningDistanceUnit" : "Point",
            "truncationMarkerCharacter" : ".",
            "truncationMinimumLength" : 1,
            "truncationPreferredCharacters" : "aeiou",
            "truncationExcludedCharacters" : "0123456789",
            "polygonAnchorPointPerimeterInsetUnit" : "Point"
          },
          "name" : "Class 1",
          "priority" : -1,
          "standardLabelPlacementProperties" : {
            "type" : "CIMStandardLabelPlacementProperties",
            "featureType" : "Line",
            "featureWeight" : "None",
            "labelWeight" : "High",
            "numLabelsOption" : "OneLabelPerName",
            "lineLabelPosition" : {
              "type" : "CIMStandardLineLabelPosition",
              "above" : true,
              "inLine" : true,
              "parallel" : true
            },
            "lineLabelPriorities" : {
              "type" : "CIMStandardLineLabelPriorities",
              "aboveStart" : 3,
              "aboveAlong" : 3,
              "aboveEnd" : 3,
              "centerStart" : 3,
              "centerAlong" : 3,
              "centerEnd" : 3,
              "belowStart" : 3,
              "belowAlong" : 3,
              "belowEnd" : 3
            },
            "pointPlacementMethod" : "AroundPoint",
            "pointPlacementPriorities" : {
              "type" : "CIMStandardPointPlacementPriorities",
              "aboveLeft" : 2,
              "aboveCenter" : 2,
              "aboveRight" : 1,
              "centerLeft" : 3,
              "centerRight" : 2,
              "belowLeft" : 3,
              "belowCenter" : 3,
              "belowRight" : 2
            },
            "rotationType" : "Arithmetic",
            "polygonPlacementMethod" : "AlwaysHorizontal"
          },
          "textSymbol" : {
            "type" : "CIMSymbolReference",
            "symbol" : {
              "type" : "CIMTextSymbol",
              "blockProgression" : "TTB",
              "depth3D" : 1,
              "extrapolateBaselines" : true,
              "fontEffects" : "Normal",
              "fontEncoding" : "Unicode",
              "fontFamilyName" : "Tahoma",
              "fontStyleName" : "Regular",
              "fontType" : "Unspecified",
              "haloSize" : 1,
              "height" : 10,
              "hinting" : "Default",
              "horizontalAlignment" : "Left",
              "kerning" : true,
              "letterWidth" : 100,
              "ligatures" : true,
              "lineGapType" : "ExtraLeading",
              "symbol" : {
                "type" : "CIMPolygonSymbol",
                "symbolLayers" : [
                  {
                    "type" : "CIMSolidFill",
                    "enable" : true,
                    "color" : {
                      "type" : "CIMRGBColor",
                      "values" : [
                        0,
                        0,
                        0,
                        100
                      ]
                    }
                  }
                ]
              },
              "textCase" : "Normal",
              "textDirection" : "LTR",
              "verticalAlignment" : "Bottom",
              "verticalGlyphOrientation" : "Right",
              "wordSpacing" : 100,
              "billboardMode3D" : "FaceNearPlane"
            }
          },
          "useCodedValue" : true,
          "visibility" : true,
          "iD" : -1
        }
      ],
      "renderer" : {
        "type" : "CIMUniqueValueRenderer",
        "colorRamp" : {
          "type" : "CIMRandomHSVColorRamp",
          "colorSpace" : {
            "type" : "CIMICCColorSpace",
            "url" : "Default RGB"
          },
          "maxH" : 360,
          "minS" : 15,
          "maxS" : 30,
          "minV" : 99,
          "maxV" : 100,
          "minAlpha" : 100,
          "maxAlpha" : 100
        },
        "defaultLabel" : "<all other values>",
        "defaultSymbol" : {
          "type" : "CIMSymbolReference",
          "symbol" : {
            "type" : "CIMPointSymbol",
            "symbolLayers" : [
              {
                "type" : "CIMVectorMarker",
                "enable" : true,
                "anchorPointUnits" : "Relative",
                "dominantSizeAxis3D" : "Z",
                "size" : 4,
                "billboardMode3D" : "FaceNearPlane",
                "frame" : {
                  "xmin" : -2,
                  "ymin" : -2,
                  "xmax" : 2,
                  "ymax" : 2
                },
                "markerGraphics" : [
                  {
                    "type" : "CIMMarkerGraphic",
                    "geometry" : {
                      "curveRings" : [
                        [
                          [
                            1.2246467991473532e-16,
                            2
                          ],
                          {
                            "a" : [
                              [
                                1.2246467991473532e-16,
                                2
                              ],
                              [
                                1.4625930824225041e-15,
                                0
                              ],
                              0,
                              1
                            ]
                          }
                        ]
                      ]
                    },
                    "symbol" : {
                      "type" : "CIMPolygonSymbol",
                      "symbolLayers" : [
                        {
                          "type" : "CIMSolidStroke",
                          "enable" : true,
                          "capStyle" : "Round",
                          "joinStyle" : "Round",
                          "lineStyle3D" : "Strip",
                          "miterLimit" : 10,
                          "width" : 0.69999999999999996,
                          "color" : {
                            "type" : "CIMRGBColor",
                            "values" : [
                              0,
                              0,
                              0,
                              100
                            ]
                          }
                        },
                        {
                          "type" : "CIMSolidFill",
                          "enable" : true,
                          "color" : {
                            "type" : "CIMRGBColor",
                            "values" : [
                              130,
                              130,
                              130,
                              100
                            ]
                          }
                        }
                      ]
                    }
                  }
                ],
                "scaleSymbolsProportionally" : true,
                "respectFrame" : true
              }
            ],
            "haloSize" : 1,
            "scaleX" : 1,
            "angleAlignment" : "Display"
          }
        },
        "defaultSymbolPatch" : "Default",
        "groups" : [
          {
            "type" : "CIMUniqueValueGroup",
            "classes" : [
              {
                "type" : "CIMUniqueValueClass",
                "label" : "Equal to WSE Grid",
                "patch" : "Default",
                "symbol" : {
                  "type" : "CIMSymbolReference",
                  "symbol" : {
                    "type" : "CIMPointSymbol",
                    "symbolLayers" : [
                      {
                        "type" : "CIMVectorMarker",
                        "enable" : true,
                        "anchorPointUnits" : "Relative",
                        "dominantSizeAxis3D" : "Z",
                        "size" : 4,
                        "billboardMode3D" : "FaceNearPlane",
                        "frame" : {
                          "xmin" : -2,
                          "ymin" : -2,
                          "xmax" : 2,
                          "ymax" : 2
                        },
                        "markerGraphics" : [
                          {
                            "type" : "CIMMarkerGraphic",
                            "geometry" : {
                              "curveRings" : [
                                [
                                  [
                                    1.2246467991473532e-16,
                                    2
                                  ],
                                  {
                                    "a" : [
                                      [
                                        1.2246467991473532e-16,
                                        2
                                      ],
                                      [
                                        1.5628715010100145e-15,
                                        0
                                      ],
                                      0,
                                      1
                                    ]
                                  }
                                ]
                              ]
                            },
                            "symbol" : {
                              "type" : "CIMPolygonSymbol",
                              "symbolLayers" : [
                                {
                                  "type" : "CIMSolidStroke",
                                  "enable" : true,
                                  "capStyle" : "Round",
                                  "joinStyle" : "Round",
                                  "lineStyle3D" : "Strip",
                                  "miterLimit" : 10,
                                  "width" : 0.69999999999999996,
                                  "color" : {
                                    "type" : "CIMRGBColor",
                                    "values" : [
                                      0,
                                      0,
                                      0,
                                      0
                                    ]
                                  }
                                },
                                {
                                  "type" : "CIMSolidFill",
                                  "enable" : true,
                                  "color" : {
                                    "type" : "CIMRGBColor",
                                    "values" : [
                                      0,
                                      0,
                                      0,
                                      100
                                    ]
                                  }
                                }
                              ]
                            }
                          }
                        ],
                        "scaleSymbolsProportionally" : true,
                        "respectFrame" : true
                      }
                    ],
                    "haloSize" : 1,
                    "scaleX" : 1,
                    "angleAlignment" : "Display"
                  }
                },
                "values" : [
                  {
                    "type" : "CIMUniqueValue",
                    "fieldValues" : [
                      "Equal to WSE Grid"
                    ]
                  }
                ],
                "visible" : true
              },
              {
                "type" : "CIMUniqueValueClass",
                "label" : "Greater than WSE Grid",
                "patch" : "Default",
                "symbol" : {
                  "type" : "CIMSymbolReference",
                  "symbol" : {
                    "type" : "CIMPointSymbol",
                    "symbolLayers" : [
                      {
                        "type" : "CIMVectorMarker",
                        "enable" : true,
                        "anchorPointUnits" : "Relative",
                        "dominantSizeAxis3D" : "Z",
                        "size" : 4,
                        "billboardMode3D" : "FaceNearPlane",
                        "frame" : {
                          "xmin" : -2,
                          "ymin" : -2,
                          "xmax" : 2,
                          "ymax" : 2
                        },
                        "markerGraphics" : [
                          {
                            "type" : "CIMMarkerGraphic",
                            "geometry" : {
                              "curveRings" : [
                                [
                                  [
                                    1.2246467991473532e-16,
                                    2
                                  ],
                                  {
                                    "a" : [
                                      [
                                        1.2246467991473532e-16,
                                        2
                                      ],
                                      [
                                        1.5628715010100145e-15,
                                        0
                                      ],
                                      0,
                                      1
                                    ]
                                  }
                                ]
                              ]
                            },
                            "symbol" : {
                              "type" : "CIMPolygonSymbol",
                              "symbolLayers" : [
                                {
                                  "type" : "CIMSolidStroke",
                                  "enable" : true,
                                  "capStyle" : "Round",
                                  "joinStyle" : "Round",
                                  "lineStyle3D" : "Strip",
                                  "miterLimit" : 10,
                                  "width" : 0.69999999999999996,
                                  "color" : {
                                    "type" : "CIMRGBColor",
                                    "values" : [
                                      0,
                                      0,
                                      0,
                                      0
                                    ]
                                  }
                                },
                                {
                                  "type" : "CIMSolidFill",
                                  "enable" : true,
                                  "color" : {
                                    "type" : "CIMRGBColor",
                                    "values" : [
                                      255,
                                      0,
                                      0,
                                      100
                                    ]
                                  }
                                }
                              ]
                            }
                          }
                        ],
                        "scaleSymbolsProportionally" : true,
                        "respectFrame" : true
                      }
                    ],
                    "haloSize" : 1,
                    "scaleX" : 1,
                    "angleAlignment" : "Display"
                  }
                },
                "values" : [
                  {
                    "type" : "CIMUniqueValue",
                    "fieldValues" : [
                      "Greater than WSE Grid"
                    ]
                  }
                ],
                "visible" : true
              },
              {
                "type" : "CIMUniqueValueClass",
                "label" : "Less than WSE Grid",
                "patch" : "Default",
                "symbol" : {
                  "type" : "CIMSymbolReference",
                  "symbol" : {
                    "type" : "CIMPointSymbol",
                    "symbolLayers" : [
                      {
                        "type" : "CIMVectorMarker",
                        "enable" : true,
                        "anchorPointUnits" : "Relative",
                        "dominantSizeAxis3D" : "Z",
                        "size" : 4,
                        "billboardMode3D" : "FaceNearPlane",
                        "frame" : {
                          "xmin" : -2,
                          "ymin" : -2,
                          "xmax" : 2,
                          "ymax" : 2
                        },
                        "markerGraphics" : [
                          {
                            "type" : "CIMMarkerGraphic",
                            "geometry" : {
                              "curveRings" : [
                                [
                                  [
                                    1.2246467991473532e-16,
                                    2
                                  ],
                                  {
                                    "a" : [
                                      [
                                        1.2246467991473532e-16,
                                        2
                                      ],
                                      [
                                        1.5628715010100145e-15,
                                        0
                                      ],
                                      0,
                                      1
                                    ]
                                  }
                                ]
                              ]
                            },
                            "symbol" : {
                              "type" : "CIMPolygonSymbol",
                              "symbolLayers" : [
                                {
                                  "type" : "CIMSolidStroke",
                                  "enable" : true,
                                  "capStyle" : "Round",
                                  "joinStyle" : "Round",
                                  "lineStyle3D" : "Strip",
                                  "miterLimit" : 10,
                                  "width" : 0.69999999999999996,
                                  "color" : {
                                    "type" : "CIMRGBColor",
                                    "values" : [
                                      0,
                                      0,
                                      0,
                                      0
                                    ]
                                  }
                                },
                                {
                                  "type" : "CIMSolidFill",
                                  "enable" : true,
                                  "color" : {
                                    "type" : "CIMRGBColor",
                                    "values" : [
                                      85,
                                      255,
                                      0,
                                      100
                                    ]
                                  }
                                }
                              ]
                            }
                          }
                        ],
                        "scaleSymbolsProportionally" : true,
                        "respectFrame" : true
                      }
                    ],
                    "haloSize" : 1,
                    "scaleX" : 1,
                    "angleAlignment" : "Display"
                  }
                },
                "values" : [
                  {
                    "type" : "CIMUniqueValue",
                    "fieldValues" : [
                      "Less than WSE Grid"
                    ]
                  }
                ],
                "visible" : true
              }
            ],
            "heading" : "BFE Values"
          }
        ],
        "valueExpressionInfo" : {
          "type" : "CIMExpressionInfo",
          "title" : "BFE Values",
          "expression" : "var base = $feature.BFE_BASE\nvar test = $feature.BLELEV1PCT\nvar s = ''\n\nif (base == null) {\n    s = null\n}\nelse if (Round(base) > test) {\n    s = 'Less than WSE Grid'\n} else if (Round(base) < test) {\n    s = 'Greater than WSE Grid'\n} else if (Round(base) == test){\n    s = 'Equal to WSE Grid'\n} \n\nreturn s",
          "returnType" : "Default"
        },
        "polygonSymbolColorTarget" : "Fill"
      },
      "scaleSymbols" : true,
      "snappable" : true,
      "symbolLayerDrawing" : {
        "type" : "CIMSymbolLayerDrawing"
      }
    }
  ],
  "elevationSurfaces" : [
    {
      "type" : "CIMMapElevationSurface",
      "elevationMode" : "BaseGlobeSurface",
      "name" : "Ground",
      "verticalExaggeration" : 1,
      "mapElevationID" : "{DE120E67-7AF3-4B4B-AE34-225EE7E70F22}",
      "color" : {
        "type" : "CIMRGBColor",
        "values" : [
          255,
          255,
          255,
          100
        ]
      },
      "surfaceTINShadingMode" : "Smooth",
      "visibility" : true,
      "expanded" : true
    }
  ],
  "rGBColorProfile" : "sRGB IEC61966-2-1 noBPC",
  "cMYKColorProfile" : "U.S. Web Coated (SWOP) v2"
}"""
def create_gdb(data_dir, report_file):
    if os.path.isdir(data_dir):
        
        #out_folder = os.path.dirname(report_file)
        gdb_name = os.path.basename(report_file)[:-4]
        gdb_path = arcpy.management.CreateFileGDB(data_dir, gdb_name)
    else:
        os.makedirs(data_dir)
        gdb_name = os.path.basename(report_file)[:-4]
        gdb_path = arcpy.management.CreateFileGDB(data_dir, gdb_name)
    return gdb_path.getOutput(0)
def unzip_data(portal, item_id):
    try:     
        #downloads_path = str(Path.home() / "Downloads")    # path to downloads folder
        data_dir = os.path.join(os.path.dirname(in_gdb), 'BLE_QAQC_Data')
        file_name = os.path.join(data_dir, 'BFE_2D_TestPoints.lyrx')
        if os.path.isfile(file_name) :
            downloaded_item = file_name
        else:
            gis = GIS(portal)
            tool_data = gis.content.get(item_id)
            zipped_tool_data = tool_data.download(data_dir)    # download the data item
            z = zipfile.ZipFile(zipped_tool_data)
            z.extractall(data_dir)
            downloaded_item = os.path.join(data_dir, 'BFE_2D_TestPoints.lyrx')     
    except Exception as e:
        print(f'Error unzipping file: {e}')
    return downloaded_item

def bfe_2d_check(test_feature, wse_01pct, report_file, in_gdb):
        data_dir = os.path.join(os.path.dirname(in_gdb), 'BLE_QAQC_Data')
        save_path = create_gdb(data_dir, report_file)
        test_index = [i[1] for i in features].index(test_feature)
        test_feature = os.path.join(in_gdb, features[test_index][0], features[test_index][1])
        wse_grid = os.path.join(in_gdb, wse_01pct)
        arcpy.SetProgressorLabel('Testing BFE_2D......')
        arcpy.AddMessage('Testing BFE_2D......')
        arcpy.management.CalculateField(test_feature, "LEN_FT", '!SHAPE!.getLength("GEODESIC", "FEET")', "PYTHON3", '', "FLOAT", "NO_ENFORCE_DOMAINS")
        arcpy.management.AddFields(test_feature, "X DOUBLE;Y DOUBLE;X_FIRST DOUBLE;Y_FIRST DOUBLE;X_LAST DOUBLE;Y_LAST DOUBLE")
        arcpy.management.CalculateFields(test_feature, "PYTHON3", "X !SHAPE!.labelPoint.X;Y !SHAPE!.labelPoint.Y", '', "NO_ENFORCE_DOMAINS")
        bfe_over_200 = arcpy.management.MakeFeatureLayer(test_feature, "BFE_2D_Layer>200FT", "LEN_FT > 200")
        arcpy.management.CalculateFields(bfe_over_200.getOutput(0), "PYTHON3", "X_FIRST '!SHAPE!.positionAlongLine(0.01, True).firstPoint.X';Y_FIRST '!SHAPE!.positionAlongLine(0.01, True).firstPoint.Y'", '', "NO_ENFORCE_DOMAINS")
        arcpy.management.CalculateFields(bfe_over_200.getOutput(0), "PYTHON3", "X_LAST '!SHAPE!.positionAlongLine(0.99, True).lastPoint.X';Y_LAST '!SHAPE!.positionAlongLine(0.99, True).lastPoint.Y'", '', "NO_ENFORCE_DOMAINS")    
        sr = arcpy.Describe(test_feature).spatialReference
        sr_project = arcpy.Raster(wse_grid).spatialReference
        transform = arcpy.ListTransformations(sr, sr_project)
        bfe_points = arcpy.management.XYTableToPoint(test_feature, os.path.join(scratch_gdb, "BFE_2D_TestPointsX"), "X", "Y", None, sr)
        bfe_points_first = arcpy.management.XYTableToPoint(test_feature, os.path.join(scratch_gdb,"BFE_2D_PointFirstX"), "X_FIRST", "Y_FIRST", None, sr)
        bfe_points_last = arcpy.management.XYTableToPoint(test_feature, os.path.join(scratch_gdb,"BFE_2D_PointLastX"), "X_LAST", "Y_LAST", None, sr)
        arcpy.management.Append([bfe_points_first, bfe_points_last], bfe_points)
        arcpy.management.DeleteField(test_feature, "X;Y;LEN_FT;X_FIRST;Y_FIRST;X_LAST;Y_LAST", "DELETE_FIELDS")
        try:
            bfe_points = arcpy.management.Project(bfe_points, os.path.join(save_path,"BFE_2D_TestPoints"), sr_project, transform[0], sr, "NO_PRESERVE_SHAPE", None, "NO_VERTICAL")
        except:
            bfe_points = arcpy.management.Project(bfe_points, os.path.join(save_path,"BFE_2D_TestPoints"), sr_project, None, sr, "NO_PRESERVE_SHAPE", None, "NO_VERTICAL")
        arcpy.sa.ExtractMultiValuesToPoints(bfe_points, f"{wse_grid} BFE_BASE", "NONE")
        arr = arcpy.da.FeatureClassToNumPyArray(bfe_points, ['BLELEV1PCT', 'BFE_BASE'])
        bfe_compare = np.round(arr['BFE_BASE']) - arr['BLELEV1PCT']
        test_points = bfe_compare[~np.isnan(bfe_compare)]
        bfe_plus = test_points[test_points > 0].size
        bfe_minus = test_points[test_points < 0].size
        bfe_compare = f'Total BFE points tested: {test_points.size:,}\nBFE points above WSE grid values: {bfe_plus:,}\nBFE points below WSE grid values: {bfe_minus:,}\n{((bfe_plus+bfe_minus)/test_points.size):.1%} of points failed'
        df = pd.read_csv(report_file, '\t')
        df.loc[df["Item Name"] == os.path.basename(test_feature), 'Mapping Value Check'] = f'Failed by {((bfe_plus+bfe_minus)/test_points.size):.1%}'
        df.to_csv(report_file, sep='\t', index=False)
        with open(report_file, "a") as report:
                report.write(bfe_compare)
        arcpy.AddMessage(f'Total BFE points tested: {test_points.size:,}')
        arcpy.AddMessage(f'BFE points below WSE grid values: {bfe_plus:,}')
        arcpy.AddMessage(f'BFE points above WSE grid values: {bfe_minus:,}')
        arcpy.AddMessage(f'{((bfe_plus+bfe_minus)/test_points.size):.1%} of points failed')
        return bfe_points
if __name__ == '__main__':
    
    in_gdb = arcpy.GetParameterAsText(0)
    report_file = arcpy.GetParameterAsText(1)
    fema_portal = r"https://fema.maps.arcgis.com/"
    item_id = '5c61c8ad50554b3ba475be3f83268945' 
    arcpy.env.workspace = in_gdb
    scratch_gdb = arcpy.env.scratchWorkspace
    feature_datasets = arcpy.ListDatasets({}, "Feature")
    features = [(ds, fc) for ds in feature_datasets for fc in arcpy.ListFeatureClasses(feature_dataset = ds)]
    raster_datasets = arcpy.ListDatasets({}, "Raster")
    rasters = [raster for raster in raster_datasets]
    if 'BFE_2D' in [i[1] for i in features] and 'BLE_WSE_01PCT' in  rasters:
        arcpy.SetProgressorLabel('Checking if BFE_2D is in the database.....')
        arcpy.AddMessage('Checking if BFE_2D is in the database.....')
        with open(report_file, "a") as report:
            report.write('\n-----------------------------------------------\nTool 3 - Results:\n-----------------------------------------------')
        test_points = bfe_2d_check('BFE_2D', 'BLE_WSE_01PCT', report_file, in_gdb)
        arcpy.SetParameter(2, test_points)
        #outsym = f"JSONRENDERER={outsym}"
        #outsym = f'JSONCIMDEF={outsym}'
        outsym = unzip_data(fema_portal, item_id)
        arcpy.SetParameterSymbology(2, outsym)
        arcpy.SetParameterAsText(3, report_file)
        arcpy.AddMessage('BFE_2D mapping value check is complete.....')
    with arcpy.EnvManager(workspace = arcpy.env.scratchWorkspace):
        to_delete = arcpy.ListFeatureClasses("*X")
        for fc in to_delete:
            arcpy.management.Delete(os.path.join(arcpy.env.scratchWorkspace, fc))
    if 'BFE_2D' not in [i[1] for i in features]: 
        arcpy.AddMessage('BFE_2D is missing from the database')
    if 'BLE_WSE_01PCT' not in rasters:
        arcpy.AddMessage('BLE_WSE_01PCT is missing from the database')
