
// We include our header, but we use quotes instead of <> to say we're including it from the local directory
#include "minMax.h"

// Then we include all of our Maya specific libraries
#include <maya/MTypeId.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnNumericData.h>
#include <maya/MPlug.h>
#include <maya/MDataHandle.h>
#include <maya/MFnPlugin.h>
#include <maya/MFnEnumAttribute.h>

// we define all of our static class members up top. Everything but the ID is placeholders till later.
// Notice the :: in C++ is similar to the . in Python to denote its part of the class
MTypeId minMax::id(0x01010)
MObject minMax::inputA;
MObject minMax::inputB;
MObject minMax::mode;
MObject minMax::output;

// Our constructor and deconstructor won't do anthing special here.
minMax::minMax() {};
minMax::~minMax() {};

// we define the compute method much like we did in Python
// It returns an MStatus and it takes a plug and datablock
MStatus minMax::compute(const MPlug& plug, MDataBlock& data)
{
  // We'll create a new status object to hold our status
  MStatus status;
  // If the plug requested isn't the output plug, return the Unkown Parameter status part of the MS namespace
  if (plug != output)
  {
    return MS::kUnknownParameter;
  }

  // get the inputA handle by using inputValue, but we also give ti a reference to our status object
  // this lets it set the status on our status boject directly.
  MDataHandle iaHandle = data.inputValue(inputA, &status);

  // If the status is anything but succesfull return the status because an error occurred
  if (status != MS::kSuccess) return status;

  // Do the same for the other plugs to get their data handles
  MDataHandle ibHandle = data.inputValue(inputB, &status);
  // However instead of manually checking the status, we can use a Macro that comes with Maya
  // Macros are bits of code that the C++ preprocessor will expand to full bits of code that do the same thing as we did above
  // i.e. checks the status and if it fails, it returns
  CHECK_MSTATUS_AND_RETURN_IT(status);

  // do the same for the other handles
  MDataHandle mHandle = data.inputValue(mode, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  MDataHandle outHandle = data.inputValue(output, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  int mode = mHandle.asInt();
  double ia = iaHandle.asDouble();
  double ib = ibHandle.asDouble();

  // create a placeholder to store our value
  double value;

  // Then calculate our output in a nice simple way
  if (mode == 1)
  {
    if (ia > ib)
    {
      value = ia;
    }
    else
    {
      value = ib;
    }
  } else
  {
    if (ia < ib)
    {
      value = ia;
    }else
    {
      value = ib;
    }
  }

  // Then just like in Python, we'll set the value and clean the plug
  outHanle.setDouble(value);
  data.setClean(plug);

  // Ginally return a succesfull status
  return MS::kSuccess;
}

// our creator function is much the same as in Python
// it returns a void pointer to the place in memory where Maya cann find a new instance of our plugin
void* minMax::creator()
{
  return new minMax();
}

// The intilize function is pretty much the same as what we wrote in Python
MStatus minMax::initialize()
{
  MFnNumericAttribue nAttr;
  MFnEnumAttribute eAttr;
  MStatus status;

  // Much like everything else we do, we need to check the status after each major step.
  // This makes sure we don't have errors. It's optional but it helps you avoi uncaught errors.
  inputA = nAttr.create("inputA", "ia", MFnNumericData::kDouble, 0.0, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);

  inputB = nAttr.create("inputB", "ib", MFnNumericData::kDouble, 0.0, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  nAttr.setStorable(true);
  nAttr.setKeyable(true);

  mode = eAttr.create("mode", "m", 0, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  eAttr.addField("min", 0);
  eAttr.addField("max", 1);
  eAttr.setStorable(true);

  output = nAttr.create("output", "out", MFnNumericData::kDouble, 0.0, &status);
  CHECK_MSTATUS_AND_RETURN_IT(status);
  nAttr.setStorable(true);
  nAttr.setWritable(true);

  status = addAttribute(inputA);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = addAttribute(inputB);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = addAttribute(mode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = addAttribute(output);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = attributeAffects(inputA, output);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = attributeAffects(inputB, output);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  status = attributeAffects(mode, output);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return MS::kSuccess;
}

// Finally we MUST define our initialize and unitialize functions
// These are pretty much identical to our Python versions

MStatus initializePlugin(MObject obj)
{
  MStatus status;
  MFnPlugin plugin(obj, "Austin Cronin", "1.0", "Any", &status)
  CHECK_MSTATUS_AND_RETURN_IT(status)

  status = plugin.registerNode(
    "minMax",
    minMax::id,
    minMax::creator,
    minMax::initialize
  );
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return MS::kSuccess;
}

MStatus uninitializePlugin(MObject obj)
{
  MStatus status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(minMax::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return MS::kSuccess;
}
