def compute_heegner_point(E, discriminant=-11):
    try:
        # Try direct Heegner point computation
        heegner = E.heegner_points(discriminant)
        point = heegner[0].point()
        return point
    except AttributeError:
        print(f"Heegner points not available for E: {E}")
        try:
            # Try computing on a quadratic twist
            E_twist = E.quadratic_twist(discriminant)
            heegner = E_twist.heegner_points(discriminant)
            point = heegner[0].point()
            print(f"Heegner point computed on twist: {point}")
            return point
        except Exception as e:
            print(f"Failed to compute Heegner point on twist: {e}")
            return None
    except Exception as e:
        print(f"Failed to compute Heegner point: {e}")
      *         return None
This patch attempts the original computation, falls back to a twist, and returns None if both fail, allowing the script to continue without crashing.
      * Update CoCalc Environment: If the method is unavailable due to an outdated SageMath version, create a new CoCalc project with a newer SageMath version (e.g., 10.2). Alternatively, install the required module manually in CoCalc’s terminal:
