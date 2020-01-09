// in C++ we can leave comments with double slashes
/* We can also leave comments inside a slash and a star */

/* Header files are used to describe the contents of the main cpp file. This lets other pieces of code know what's available
 * and refers to. It also allows for functions to refer functions that hfaven't been implemented yet, by just referencing their declaration here. */

 /* At the top of most header files you'll see a ifndef followed by a define
  * The ifndef says that if this unique name is not defined, then define it and define the rest of the stuff inside it.
  * We then end the file with the endif for this ifndef.
  * This is called a preprocessor guard
  * This prevents the same header file from being included many times which can drastically help compiling time.
  */

#ifndef MAYA_MINMAX_H
#define MAYA_MINMAX_H

// AFter the declaration, we ned to include any thing we may be using. This is like importing in Python but more specific
// using the < > tells the compiler to look in the include directores we defined in our CMakeLists.txt
#include <maya/MPxNode.h>

// Now we define our minMax class and tell it to inherit from the MPxNode base
class minMax : public MPxNode
{
  // the public keyword means that this will be available publicaly and not hidden to tother code
public:
  minMax(); // This is the constructor called when the object is made
  ~minmax() override; // This is te destructor called when the object is destoryed from memory

  // we define the compute function and say it returns and MStatus
  // we must define wht data types it takes, and say it takes them as references. By saying const, we promise not to modify the plug.
  // This is also overriding the origingal MPxNodes compute functions
  MStatus compute(const MPlug& plug, MDataBlock& data) override;

  // The creator returns a void pointer to the new minMax object in memory
  // by declaring it static, it's  similar to the staticmethod and classmethod in Python
  // This means it doesnt need an instance of minMax to exist when called
  static void* creator();

  // The initializatino function is also static and returns an MStatus
  static MStatus initialize();

  // These are the inputs and outputs for the node
  static MObject inputA;
  static MObject inputB;
  static MObject mode;
  static MObject output;

  // This is the id of the node
  static MTypeId id;
};

// Finally we end the preprocessor guard
#endif
